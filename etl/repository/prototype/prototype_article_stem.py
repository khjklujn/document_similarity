import model
import util

from ..repository import Repository


class PrototypeArticleStem(Repository):
    def __init__(self, config: util.Config):
        super().__init__(
            model.odoo.prototype.PrototypeArticleStem,
            [
                'prototype_article_id',
                'stem_id'
            ],
            config
        )

    def by_prototype_article_id(self, key: int) -> list:
        return self._by_unique('prototype_article_id')(key)
