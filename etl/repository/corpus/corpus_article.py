import model
import util

from ..repository import Repository


class CorpusArticle(Repository):
    def __init__(self, config: util.Config):
        super().__init__(
            model.odoo.corpus.CorpusArticle,
            [
                'corpus_id',
                'unique_id'
            ],
            config
        )

    def by_corpus_id(self, key: int) -> list:
        return self._by_unique('corpus_id')(key)

    def by_id(self, key: int) -> model.odoo.corpus.CorpusArticle:
        return self._by_unique('id')(key)[0]

    def by_name(self, key: str) -> list:
        return self._by_unique('name')(key)

    def by_read_status(self, key: str) -> list:
        return self._by_unique('read_status')(key)

    def by_unique_id(self, key: str) -> model.odoo.corpus.CorpusArticle:
        return self._by_unique('unique_id')(key)[0]
