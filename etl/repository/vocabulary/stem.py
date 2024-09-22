import model
import util

from ..repository import Repository


class Stem(Repository):
    def __init__(self, config: util.Config):
        super().__init__(
            model.odoo.vocabulary.Stem,
            [
                'name'
            ],
            config
        ),

    def by_id(self, key: str) -> model.odoo.vocabulary.Stem:
        return self._by_unique('id')(key)[0]

    def by_name(self, key: str) -> model.odoo.vocabulary.Stem:
        return self._by_unique('name')(key)[0]
