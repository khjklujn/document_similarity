import model
import util

from ..repository import Repository


class PrototypeArticleCorpusArticle(Repository):
    def __init__(self, config: util.Config):
        super().__init__(
            model.odoo.prototype.PrototypeArticleCorpusArticle,
            [
                'prototype_article_id',
                'corpus_article_id'
            ],
            config
        )
