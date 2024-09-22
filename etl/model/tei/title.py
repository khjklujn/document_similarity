from dataclasses import dataclass

from lxml import etree
from ruamel.yaml import yaml_object  # type: ignore

from .replacement import down_encode
from .text import Text
from .yaml import yaml


@yaml_object(yaml)
@dataclass
class Title:
    text: Text

    @classmethod
    def from_tei(cls, article: etree.ElementTree):
        title = ''
        for element in article.iter():
            if element.tag == '{http://www.tei-c.org/ns/1.0}titleStmt':
                title = down_encode(' '.join(element.itertext()))
                break

        return cls(
            text=Text.from_text(title.strip())
        )

    @property
    def extracted_html(self):
        return f'<h1>{self.text.extracted_html}</h1>'

    @property
    def characterized_html(self):
        return f'<h1>{self.text.characterized_html}'
