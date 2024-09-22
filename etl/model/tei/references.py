from dataclasses import dataclass
from typing import List

from lxml import etree
from ruamel.yaml import yaml_object  # type: ignore

from .reference import Reference
from .yaml import yaml


@yaml_object(yaml)
@dataclass
class References:
    references: List[Reference]

    @classmethod
    def from_tei(cls, article: etree.ElementTree):
        references = []
        for element in article.iter():
            if element.tag == '{http://www.tei-c.org/ns/1.0}listBibl':
                for reference in element.iter():
                    if reference.tag == '{http://www.tei-c.org/ns/1.0}biblStruct':
                        references.append(Reference.from_tei(reference))

        return cls(references)
