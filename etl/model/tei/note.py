from dataclasses import dataclass

from ruamel.yaml import yaml_object  # type: ignore

from .text import Text
from .yaml import yaml


@yaml_object(yaml)
@dataclass
class Note:
    text: Text
