from dataclasses import dataclass
from typing import List

from ruamel.yaml import yaml_object  # type: ignore

from .paragraph import Paragraph
from .text import Text
from .yaml import yaml


@yaml_object(yaml)
@dataclass
class Section:
    heading: Text
    paragraphs: List[Paragraph]

    @property
    def extracted_html(self):
        ret = [f'<h2>{self.heading.extracted_html}</h2>']

        for paragraph in self.paragraphs:
            ret += [f'<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{paragraph.extracted_html}</p>']

        return '\n'.join(ret)

    @property
    def characterized_html(self):
        ret = [f'<h2>{self.heading.characterized_html}</h2>']

        ret += [
            f'<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{paragraph.characterized_html}</p>'
            for paragraph in self.paragraphs
        ]

        return '\n'.join(ret)
