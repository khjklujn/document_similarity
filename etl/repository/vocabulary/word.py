import model
import util

from ..repository import Repository


class Word(Repository):
    def __init__(self, config: util.Config):
        super().__init__(
            model.odoo.vocabulary.Word,
            [
                'name'
            ],
            config
        )

    def by_name(self, key: str) -> model.odoo.vocabulary.Word:
        return self._by_unique('name')(key)[0]

