from dataclasses import dataclass

from ruamel.yaml import yaml_object  # type: ignore

from .text import Text
from .yaml import yaml


@yaml_object(yaml)
@dataclass
class Keyword:
    text: Text

    @classmethod
    def from_text(cls, text: str):
        return cls(
            text=Text.from_text(text)
        )

    @property
    def extracted_html(self):
        return self.text.extracted_html

    @property
    def characterized_html(self):
        return self.text.characterized_html
