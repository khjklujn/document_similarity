import requests
import wikipedia

import util

from ..node import Node
from ..paragraph import Paragraph
from ..section import Section


class Article(Node):
    def __init__(self, page_name: str, config: util.Config):
        super().__init__(None)

        self._name = page_name
        self._unique_id = str(self.get_article_id(page_name))

        text = self.get_text(page_name, config)

        heading = Section(self, page_name)
        for line in text.split('\n'):
            if not line.strip():
                continue

            if line.startswith('='):
                heading = Section(self, line.replace('=', '').strip())
            else:
                Paragraph(heading, line.strip())

    def get_article_id(self, page_name: str) -> int:
        sections = requests.get(f'https://en.wikipedia.org/w/api.php?action=parse&format=json&prop=sections&page={page_name}')
        try:
            return sections.json()['parse']['pageid']
        except Exception:
            return 0

    def get_text(self, page_name: str, config: util.Config) -> str:
        try:
            article = wikipedia.page(page_name)
            return article.content.replace(')s', '')
        except (wikipedia.DisambiguationError, wikipedia.PageError):
            return ''

    @property
    def characterized_html(self):
        return '\n'.join(
            [
                child.characterized_html
                for child in self.children
            ]
        )

    @property
    def dependency_to_words(self) -> dict:  # type: ignore
        ret: dict = {}
        for child in self.children:
            child.dependency_to_words(ret)
        return ret

    @property
    def lemma_characterization(self) -> dict:  # type: ignore
        ret: dict = {}
        for child in self.children:
            child.lemma_characterization(ret)
        return ret

    @property
    def lemma_to_words(self) -> dict:  # type: ignore
        ret: dict = {}
        for child in self.children:
            child.lemma_to_words(ret)
        return ret

    @property
    def name(self) -> str:
        return self._name

    @property
    def stem_characterization(self) -> dict:  # type: ignore
        ret: dict = {}
        for child in self.children:
            child.stem_characterization(ret)
        return ret

    @property
    def stem_to_words(self) -> dict:  # type: ignore
        ret: dict = {}
        for child in self.children:
            child.stem_to_words(ret)
        return ret

    @property
    def text_html(self):
        return '\n'.join(
            [
                child.text_html
                for child in self.children
            ]
        )

    @property
    def token_count(self) -> dict:  # type: ignore
        ret: dict = {}
        for child in self.children:
            child.token_count(ret)
        return ret

    @property
    def unique_id(self) -> str:
        return self._unique_id
