import hashlib
import traceback

import model
import repository
import session
import util

from ..node import Node

from .abstract import Abstract
from .appendix import Appendix
from .body import Body
from .keywords import Keywords
from .title import Title


class Article(Node):
    _months = {
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

    def __init__(self, source_file: str, config: util.Config):
        super().__init__(None)
        self._file_name = source_file.replace(config.source_root, '')
        self._parsing_succeeded = True

        with open(source_file, 'rb') as file_in:
            self._unique_id = hashlib.sha3_512(file_in.read()).hexdigest()

        try:
            with session.Grobid(config) as grobid:
                tei = grobid.session.process_full_text(source_file)
        except Exception:
            self._parsing_succeeded = False
            load_failures = repository.corpus.LoadFailure(config)
            load_failures.add(
                model.odoo.corpus.LoadFailure(
                    self._file_name,
                    self._unique_id,
                    'GROBID Parse',
                    traceback.format_exc()
                )
            )
            load_failures.upsert_many()
            return

        try:
            self._journal = self._file_name.split('/')[0]
            self._year = self._file_name.split('/')[1].split(' ')[0]
        except Exception:
            self._parsing_succeeded = False
            load_failures = repository.corpus.LoadFailure(config)
            load_failures.add(
                model.odoo.corpus.LoadFailure(
                    self._file_name,
                    self._unique_id,
                    'From Filename',
                    traceback.format_exc()
                )
            )
            load_failures.upsert_many()
            return

        try:
            self._title = Title(self, tei)
        except Exception:
            self._parsing_succeeded = False
            load_failures = repository.corpus.LoadFailure(config)
            load_failures.add(
                model.odoo.corpus.LoadFailure(
                    self._file_name,
                    self._unique_id,
                    'Parse Title',
                    traceback.format_exc()
                )
            )
            load_failures.upsert_many()
            return

        try:
            self._abstract = Abstract(self, tei)
        except Exception:
            self._parsing_succeeded = False
            load_failures = repository.corpus.LoadFailure(config)
            load_failures.add(
                model.odoo.corpus.LoadFailure(
                    self._file_name,
                    self._unique_id,
                    'Parse Abstract',
                    traceback.format_exc()
                )
            )
            load_failures.upsert_many()
            return

        try:
            self._keywords = Keywords(self, tei)
        except Exception:
            self._parsing_succeeded = False
            load_failures = repository.corpus.LoadFailure(config)
            load_failures.add(
                model.odoo.corpus.LoadFailure(
                    self._file_name,
                    self._unique_id,
                    'Parse Keywords',
                    traceback.format_exc()
                )
            )
            load_failures.upsert_many()
            return

        try:
            self._body = Body(self, tei)
        except Exception:
            self._parsing_succeeded = False
            load_failures = repository.corpus.LoadFailure(config)
            load_failures.add(
                model.odoo.corpus.LoadFailure(
                    self._file_name,
                    self._unique_id,
                    'Parse Body',
                    traceback.format_exc()
                )
            )
            load_failures.upsert_many()
            return

        try:
            self._appendix = Appendix(self, tei)
        except Exception:
            self._parsing_succeeded = False
            load_failures = repository.corpus.LoadFailure(config)
            load_failures.add(
                model.odoo.corpus.LoadFailure(
                    self._file_name,
                    self._unique_id,
                    'Parse Appendix',
                    traceback.format_exc()
                )
            )
            load_failures.upsert_many()
            return

    @property
    def characterized_html(self):
        return '\n'.join(
            (
                self.title.characterized_html,
                self.keywords.characterized_html,
                self.abstract.characterized_html,
                self.body.characterized_html,
                self.appendix.characterized_html,
            )
        )

    @property
    def abstract(self) -> Abstract:
        return self._abstract

    @property
    def appendix(self) -> Appendix:
        return self._appendix

    @property
    def body(self) -> Body:
        return self._body

    @property
    def dependency_to_words(self) -> dict:  # type: ignore
        ret: dict = {}
        for child in self.children:
            child.dependency_to_words(ret)
        return ret

    @property
    def file_name(self) -> str:
        return self._file_name

    @property
    def journal(self) -> str:
        return self._journal

    @property
    def keywords(self) -> Keywords:
        return self._keywords

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
    def parsing_succeeded(self):
        return self._parsing_succeeded

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
            (
                self.title.text_html,
                self.keywords.text_html,
                self.abstract.text_html,
                self.body.text_html,
                self.appendix.characterized_html,
            )
        )

    @property
    def title(self) -> Title:
        return self._title

    @property
    def token_count(self) -> dict:  # type: ignore
        ret: dict = {}
        for child in self.children:
            child.token_count(ret)
        return ret

    @property
    def year(self) -> str:
        return self._year

    @property
    def unique_id(self) -> str:
        return self._unique_id
