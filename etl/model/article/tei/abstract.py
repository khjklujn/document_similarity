from lxml import etree

from ..node import Node
from ..paragraph import Paragraph
from ..section import Section


class Abstract(Section):
    def __init__(self, parent: Node, tei: etree.ElementTree):
        super().__init__(parent, 'Abstract')

        for element in tei.iter():
            if element.tag == '{http://www.tei-c.org/ns/1.0}abstract':
                for paragraph in element.iter():
                    if paragraph.tag == '{http://www.tei-c.org/ns/1.0}p':
                        Paragraph(self, ' '.join(paragraph.itertext()))
                break


