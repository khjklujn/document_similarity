import model
import util

from ..repository import Repository


class PrototypeArticle(Repository):
    def __init__(self, config: util.Config):
        super().__init__(
            model.odoo.prototype.PrototypeArticle,
            [
                'topic_id',
                'unique_id',
            ],
            config
        )

    def by_name(self, key: str) -> list:
        return self._by_unique('name')(key)

    def by_topic_id(self, key: int) -> list:
        return self._by_unique('topic_id')(key)
