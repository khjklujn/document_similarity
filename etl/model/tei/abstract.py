from dataclasses import dataclass
from typing import List

from lxml import etree
from ruamel.yaml import yaml_object  # type: ignore

from .paragraph import Paragraph
from .yaml import yaml


@yaml_object(yaml)
@dataclass
class Abstract:
    paragraphs: List[Paragraph]

    @classmethod
    def from_tei(cls, article: etree.ElementTree):
        paragraphs = []
        for element in article.iter():
            if element.tag == '{http://www.tei-c.org/ns/1.0}abstract':
                for paragraph in element.iter():
                    if paragraph.tag == '{http://www.tei-c.org/ns/1.0}p':
                        paragraphs.append(
                            Paragraph.from_text(
                                kind='Abstract',
                                text=' '.join(paragraph.itertext())
                            )
                        )
                break

        return cls(
            paragraphs=paragraphs
        )

    @property
    def extracted_html(self):
        ret = ['<h2>Abstract</h2>']

        ret += [
            f'<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{paragraph.extracted_html}</p>'
            for paragraph in self.paragraphs
        ]

        return '\n'.join(ret)

    @property
    def characterized_html(self):
        ret = ['<h2><font color="#CFCFCF">abstract</font></h2>']

        ret += [
            f'<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{paragraph.characterized_html}</p>'
            for paragraph in self.paragraphs
        ]

        return '\n'.join(ret)
