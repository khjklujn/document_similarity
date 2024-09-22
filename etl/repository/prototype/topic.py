import model
import util

from ..repository import Repository


class Topic(Repository):
    def __init__(self, config: util.Config):
        super().__init__(
            model.odoo.prototype.Topic,
            [
                'name'
            ],
            config
        )

    def by_name(self, key: str) -> model.odoo.prototype.Topic:
        return self._by_unique('name')(key)[0]
