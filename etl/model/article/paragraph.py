from .node import Node
from .sentences import Sentences


class Paragraph(Sentences):
    def __init__(self, parent: Node, text: str):
        super().__init__(parent, text)

    @property
    def characterized_html(self):
        return f'<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {super().characterized_html} </p>'

    @property
    def text_html(self):
        return f'<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {super().text_html} </p>'
