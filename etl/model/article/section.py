from typing import Optional

from .node import Node
from .sentences import Sentences


class Section(Node):
    def __init__(self, parent: Optional[Node], text: str):
        super().__init__(parent)

        self._heading = Sentences(None, text)

    def lemma_characterization(self, accumulator: dict = None) -> dict:
        if accumulator is None:
            accumulator = {}
        for child in self.children:
            child.lemma_characterization(accumulator)
        self.heading.lemma_characterization(accumulator)
        return accumulator

    def stem_characterization(self, accumulator) -> dict:
        for child in self.children:
            child.stem_characterization(accumulator)
        self.heading.stem_characterization(accumulator)
        return accumulator

    def stem_to_words(self, accumulator) -> dict:
        for child in self.children:
            child.stem_to_words(accumulator)
        self.heading.stem_to_words(accumulator)
        return accumulator

    def token_count(self, accumulator: dict = None) -> dict:
        if accumulator is None:
            accumulator = {}
        for child in self.children:
            child.token_count(accumulator)
        self.heading.token_count(accumulator)
        return accumulator

    @property
    def characterized_html(self):
        ret = [f'<h2> {self.heading.characterized_html} </h2>']
        ret += [
            paragraph.characterized_html
            for paragraph in self.children
        ]
        return '\n'.join(ret)

    @property
    def heading(self):
        return self._heading

    @property
    def text_html(self):
        ret = [f'<h2> {self.heading.text_html} </h2>']
        ret += [
            paragraph.text_html
            for paragraph in self.children
        ]
        return '\n'.join(ret)
