from dataclasses import dataclass

from lxml import etree
from ruamel.yaml import yaml_object  # type: ignore

from .replacement import down_encode
from .yaml import yaml


@yaml_object(yaml)
@dataclass
class Author:
    forename: str
    middlename: str
    surname: str

    @classmethod
    def from_tei(cls, section: etree.ElementTree):
        forename = ''
        middlename = ''
        surname = ''
        for author in section.iter():
            if author.tag == '{http://www.tei-c.org/ns/1.0}forename' and author.attrib.get('type', None) == 'first':
                forename = down_encode(' '.join(author.itertext()))
            if author.tag == '{http://www.tei-c.org/ns/1.0}forename' and author.attrib.get('type', None) == 'middle':
                middlename = down_encode(' '.join(author.itertext()))
            if author.tag == '{http://www.tei-c.org/ns/1.0}surname':
                surname = down_encode(' '.join(author.itertext()))

        return cls(
            forename=forename,
            middlename=middlename,
            surname=surname
        )
