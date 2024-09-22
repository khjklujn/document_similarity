from dataclasses import dataclass

from lxml import etree
from ruamel.yaml import yaml_object  # type: ignore

from .abstract import Abstract
from .appendix import Appendix
from .body import Body
from .keywords import Keywords
from .title import Title
from .yaml import yaml


@yaml_object(yaml)
@dataclass
class Article:
    source_file: str
    publication: str
    volume: str
    issue: str
    year: str
    month: str
    title: Title
    abstract: Abstract
    keywords: Keywords
    body: Body
    appendix: Appendix
    sha512: str

    @classmethod
    def from_source(cls, source_root: str, source_file: str, sha512: str, article: etree.ElementTree):
        file_name = source_file.replace(source_root, '')
        publication = file_name.split('/')[0]
        year = file_name.split('/')[1].split(' ')[0]
        volume = file_name.split('/')[2].split(' ')[1].zfill(3)
        issue = file_name.split('/')[2].split(' ')[3].zfill(2)
        months = {
            'Jan': '01 JAN',
            'Feb': '02 FEB',
            'Mar': '03 MAR',
            'Apr': '04 APR',
            'May': '05 MAY',
            'Jun': '06 JUN',
            'Jul': '07 JUL',
            'Aug': '08 AUG',
            'Sep': '09 SEP',
            'Oct': '10 OCT',
            'Nov': '11 NOV',
            'Dec': '12 DEC',
        }
        month = months[file_name.split('/')[2].split(' ')[4]]
        title = Title.from_tei(article)
        abstract = Abstract.from_tei(article)
        keywords = Keywords.from_tei(article)
        body = Body.from_tei(article)
        appendix = Appendix.from_tei(article)

        return cls(
            source_file=file_name,
            publication=publication,
            year=year,
            volume=volume,
            issue=issue,
            month=month,
            title=title,
            abstract=abstract,
            keywords=keywords,
            body=body,
            appendix=appendix,
            sha512=sha512
        )

    @property
    def extracted_html(self):
        return '\n'.join(
            (
                self.title.extracted_html,
                self.keywords.extracted_html,
                self.abstract.extracted_html,
                self.body.extracted_html,
                self.appendix.extracted_html
            )
        )

    @property
    def characterized_html(self):
        return '\n'.join(
            (
                self.title.characterized_html,
                self.keywords.characterized_html,
                self.abstract.characterized_html,
                self.body.characterized_html,
                self.appendix.characterized_html
            )
        )
