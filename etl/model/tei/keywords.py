from typing import List
from dataclasses import dataclass

from lxml import etree
from ruamel.yaml import yaml_object  # type: ignore

from .keyword import Keyword
from .yaml import yaml


@yaml_object(yaml)
@dataclass
class Keywords:
    kind: str
    keywords: List[Keyword]

    @classmethod
    def from_tei(cls, article: etree.ElementTree):
        kind = 'none'
        out = []
        for element in article.iter():
            if element.tag == '{http://www.tei-c.org/ns/1.0}keywords':
                if element.getchildren():
                    kind = 'parsed'
                    for keyword in element.iter():
                        out.append(
                            Keyword.from_text(
                                ' '.join(keyword.itertext())
                            )
                        )
                else:
                    kind = 'unparsed'
                    out = [
                        Keyword.from_text(
                            ' '.join(element.itertext())
                        )
                    ]
                break

        return cls(
            kind=kind,
            keywords=out
        )

    @property
    def extracted_html(self):
        return ' '.join([keyword.extracted_html for keyword in self.keywords])

    @property
    def characterized_html(self):
        return ' '.join([keyword.characterized_html for keyword in self.keywords])
