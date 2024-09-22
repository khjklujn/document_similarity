from lxml import etree

from ..node import Node
from ..sentences import Sentences


class Title(Sentences):
    def __init__(self, parent: Node, tei: etree.ElementTree):
        title = ''
        for element in tei.iter():
            if element.tag == '{http://www.tei-c.org/ns/1.0}titleStmt':
                title = ' '.join(element.itertext())
                break

        super().__init__(parent, title)

    @property
    def characterized_html(self):
        return f'<h1> {" ".join((item.characterized_html for item in self.original_order))} </h1>'

    @property
    def text(self):
        return f'{" ".join((item.text_html for item in self.original_order))}'

    @property
    def text_html(self):
        return f'<h1> {" ".join((item.text_html for item in self.original_order))} </h1>'
