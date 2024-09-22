import model
import util

from ..repository import Repository


class CorpusArticleStem(Repository):
    def __init__(self, config: util.Config):
        super().__init__(
            model.odoo.corpus.CorpusArticleStem,
            [
                'corpus_article_id',
                'stem_id'
            ],
            config
        )

    def by_corpus_article_id(self, key: int) -> list:
        return self._by_unique('corpus_article_id')(key)

