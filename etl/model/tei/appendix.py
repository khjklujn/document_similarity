from dataclasses import dataclass
from typing import List

from lxml import etree
from ruamel.yaml import yaml_object  # type: ignore

from .note import Note
from .paragraph import Paragraph
from .section import Section
from .text import Text
from .yaml import yaml


@yaml_object(yaml)
@dataclass
class Appendix:
    sections: List[Section]
    notes: List[Note]

    @classmethod
    def from_tei(cls, article: etree.ElementTree):
        sections = []
        notes = []
        keywords_in_appendix = False
        for element in article.iter():
            if element.attrib.get('type', None) == 'annex':
                for item in element.getchildren():
                    if element.tag == '{http://www.tei-c.org/ns/1.0}div':
                        heading = ''
                        paragraphs = []
                        for entry in item.iter():
                            if entry.tag == '{http://www.tei-c.org/ns/1.0}head':
                                heading = ' '.join(entry.itertext())
                                keywords_in_appendix |= 'Keywords' in heading
                            if entry.tag == '{http://www.tei-c.org/ns/1.0}p':
                                paragraph = Paragraph.from_text(
                                    kind='Appendix',
                                    text=' '.join(entry.itertext())
                                )
                                paragraphs.append(paragraph)

                        sections.append(
                            Section(
                                heading=Text.from_text(heading),
                                paragraphs=paragraphs
                            )
                        )

                    if element.tag == '{http://www.tei-c.org/ns/1.0}note':
                        note_text = ' '.join(entry.itertext())
                        notes.append(
                            Note(
                                text=Text.from_text(note_text)
                            )
                        )

        return cls(
            sections=sections,
            notes=notes
        )

    @property
    def extracted_html(self):
        return '\n'.join(
            [
               f'<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{section.extracted_html}</p>'
               for section in self.sections
            ]
        )

    @property
    def characterized_html(self):
        return '\n'.join(
            [
               f'<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{section.characterized_html}</p>'
               for section in self.sections
            ]
        )
