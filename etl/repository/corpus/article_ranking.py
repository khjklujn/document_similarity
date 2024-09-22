import model
import util

from ..repository import Repository


class ArticleRanking(Repository):
    def __init__(self, config: util.Config):
        super().__init__(
            model.odoo.corpus.ArticleRanking,
            [
                'corpus_article_id'
            ],
            config
        )
