import model
import util

from ..repository import Repository


class Corpus(Repository):
    def __init__(self, config: util.Config):
        super().__init__(
            model.odoo.corpus.Corpus,
            [
                'name'
            ],
            config
        )

    def by_name(self, key: str) -> model.odoo.corpus.Corpus:
        return self._by_unique('name')(key)[0]
