from typing import Optional

from . import dependency
from .nlp import NLP
from .node import Node
from .scrub import scrub


class Sentences(Node):
    def __init__(self, parent: Optional[Node], text: str):
        super().__init__(parent)
        self._text = text

        tokens = NLP(scrub(text))
        [
            dependency.Root.walk_sentence(self, sentence.root)
            for sentence in tokens.sents
        ]

    @property
    def characterized_html(self):
        return ' '.join((item.characterized_html for item in self.original_order))

    @property
    def original_order(self):
        ret: list = []
        for child in self.children:
            ordered = child.original_order
            ordered.sort()
            ret += [
                token
                for _, token in ordered
            ]
        return ret

    @property
    def text_html(self):
        return ' '.join((item.text_html for item in self.original_order))
