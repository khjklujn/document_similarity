from lxml import etree

from ..node import Node
from ..paragraph import Paragraph
from ..section import Section


class Body(Node):
    def __init__(self, parent: Node, tei: etree.ElementTree):
        super().__init__(parent)

        section = Section(self, '')
        for maybe_body in tei.iter():
            if maybe_body.tag == '{http://www.tei-c.org/ns/1.0}body':
                for element in maybe_body.iter():
                    if element.tag == '{http://www.tei-c.org/ns/1.0}div':
                        for entry in element.iter():
                            if entry.tag == '{http://www.tei-c.org/ns/1.0}head':
                                section = Section(self, ' '.join(entry.itertext()))
                            if entry.tag == '{http://www.tei-c.org/ns/1.0}p':
                                Paragraph(section, ' '.join(entry.itertext()))

                break

    @property
    def characterized_html(self):
        return '\n'.join(
            [
                heading.characterized_html
                for heading in self.children
            ]
        )

    @property
    def text_html(self):
        return '\n'.join(
            [
                heading.text_html
                for heading in self.children
            ]
        )
