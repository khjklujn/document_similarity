from dataclasses import dataclass
from typing import List

from lxml import etree
from ruamel.yaml import yaml_object  # type: ignore

from .author import Author
from .yaml import yaml


@yaml_object(yaml)
@dataclass
class Authors:
    authors: List[Author]

    @classmethod
    def from_tei(cls, article: etree.ElementTree):
        authors = []
        for element in article.iter():
            if element.tag == '{http://www.tei-c.org/ns/1.0}sourceDesc':
                for maybe_author in element.iter():
                    if maybe_author.tag == '{http://www.tei-c.org/ns/1.0}author':
                        author = Author.from_tei(maybe_author)
                        if author.forename or author.middlename or author.surname:
                            authors.append(author)

        return cls(authors)
