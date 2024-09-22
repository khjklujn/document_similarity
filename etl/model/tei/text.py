from dataclasses import dataclass
import typing

from ruamel.yaml import yaml_object  # type: ignore

from .nlp import nlp
from .replacement import down_encode
from .token import Token
from .yaml import yaml


@yaml_object(yaml)
@dataclass
class Text:
    text: str
    tokens: typing.List[Token]

    @classmethod
    def from_text(cls, text: str):
        scrubbed = (
            down_encode(text)
            .replace("'", " ' ")
            .replace(r'%', r' %')
            .replace('_', ' _ ')
            .replace('`', ' ` ')
            .replace('1', ' 1 ')
            .replace('2', ' 2 ')
            .replace('3', ' 3 ')
            .replace('4', ' 4 ')
            .replace('5', ' 5 ')
            .replace('6', ' 6 ')
            .replace('7', ' 7 ')
            .replace('8', ' 8 ')
            .replace('9', ' 9 ')
            .replace('0', ' 0 ')
            .replace('~', ' ~ ')
            .replace('!', ' ! ')
            .replace('@', ' @ ')
            .replace('#', ' # ')
            .replace('$', ' $ ')
            .replace('^', ' ^ ')
            .replace('*', ' * ')
            .replace('[', ' [ ')
            .replace(']', ' ] ')
            .replace('\\', ' ')
            .replace('|', ' | ')
            .replace('(', ' ( ')
            .replace(')', ' ) ')
            .replace('=', ' = ')
            .replace('.', ' . ')
            .replace('>', ' > ')
            .replace('<', ' < ')
            .replace(';', ' ; ')
            .replace(':', ' : ')
            .replace('!', ' ! ')
            .replace('?', ' ? ')
            .replace('[', ' [ ')
            .replace(']', ' ] ')
            .replace('{', ' { ')
            .replace('}', ' } ')
            .replace('+', ' + ')
            .replace('-', ' - ')
            .replace('"', ' " ')
            .replace(',', ' , ')
            .replace('/', ' / ')
        )
        document = nlp(scrubbed)

        tokens = [
            Token.from_token(token)
            for token in document
            if token.text.strip()
        ]

        return cls(
            text=text,
            tokens=tokens
        )

    @property
    def extracted_html(self):
        return self.text

    @property
    def characterized_html(self):
        return ' '.join(
            [
                token.characterized_html
                for token in self.tokens
            ]
        )
