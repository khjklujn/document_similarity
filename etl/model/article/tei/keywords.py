from lxml import etree

from ..node import Node
from ..sentences import Sentences


class Keywords(Sentences):
    def __init__(self, parent: Node, tei: etree.ElementTree):
        text = ''
        for element in tei.iter():
            if element.tag == '{http://www.tei-c.org/ns/1.0}keywords':
                if element.getchildren():
                    for keyword in element.iter():
                        text += f' {" ".join(keyword.itertext())}'
                else:
                    text += ' '.join(element.itertext())
                break

        super().__init__(parent, text)


