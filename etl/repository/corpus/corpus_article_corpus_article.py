import model
import util

from ..repository import Repository


class CorpusArticleCorpusArticle(Repository):
    def __init__(self, config: util.Config):
        super().__init__(
            model.odoo.corpus.CorpusArticleCorpusArticle,
            [
                'prototype_article_id',
                'corpus_article_id'
            ],
            config
        )
