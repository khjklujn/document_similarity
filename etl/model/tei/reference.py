from dataclasses import dataclass
from typing import List

from lxml import etree
from ruamel.yaml import yaml_object  # type: ignore

from .author import Author
from .replacement import down_encode
from .text import Text
from .title import Title
from .yaml import yaml


@yaml_object(yaml)
@dataclass
class Reference:
    title: Title
    authors: List[Author]
    publication: str
    volume: str
    issue: str
    year: str

    @classmethod
    def from_tei(cls, section: etree.ElementTree):
        title = Title(
            text=Text.from_text('NO TITLE FOUND')
        )
        authors = []
        for element in section.iter():
            if element.tag == '{http://www.tei-c.org/ns/1.0}analytic':
                for item in element.iter():
                    if item.tag == '{http://www.tei-c.org/ns/1.0}title':
                        title = Title(
                            text=Text.from_text(
                                down_encode(' '.join(item.itertext()))
                            )
                        )
                    if item.tag == '{http://www.tei-c.org/ns/1.0}author':
                        authors.append(Author.from_tei(item))
                break

        for element in section.iter():
            publication = ''
            volume = ''
            issue = ''
            year = ''
            if element.tag == '{http://www.tei-c.org/ns/1.0}monogr':
                for item in element.iter():
                    if item.tag == '{http://www.tei-c.org/ns/1.0}title':
                        publication = down_encode(' '.join(item.itertext()))
                    if item.tag == '{http://www.tei-c.org/ns/1.0}biblScope' and item.attrib.get('unit', None) == 'volume':
                        volume = down_encode(' '.join(item.itertext())).zfill(3)
                    if item.tag == '{http://www.tei-c.org/ns/1.0}biblScope' and item.attrib.get('unit', None) == 'issue':
                        issue = down_encode(' '.join(item.itertext())).strip().zfill(2)
                    if item.tag == '{http://www.tei-c.org/ns/1.0}date':
                        year = item.attrib.get(
                            'when',
                            down_encode(' '.join(item.itertext()))
                        )

                break

        return cls(
            title=title,
            authors=authors,
            publication=publication,
            volume=volume,
            issue=issue,
            year=year
        )
