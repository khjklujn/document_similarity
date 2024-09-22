import model
import util

from ..repository import Repository


class LoadFailure(Repository):
    def __init__(self, config: util.Config):
        super().__init__(
            model.odoo.corpus.LoadFailure,
            [
                'unique_id',
                'reason'
            ],
            config
        )
