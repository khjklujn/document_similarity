import logging

from odoo import fields, models

_logger = logging.getLogger(__file__)


class Stem(models.Model):
    _name = 'articles.stem'
    _description = 'Stems'
    _order = 'name'

    name = fields.Char(
        required=True,
        index=True,
        readonly=True
    )

    active = fields.Boolean(
        required=True,
        default=True
    )

    word_ids = fields.One2many(
        'articles.word',
        'stem_id',
        readonly=True,
        string='Word'
    )

    weight = fields.Float(
        digits=(6, 5),
        required=True,
        readonly=True,
        default=1.0
    )

    _sql_constraints = [
        (
            'name_unique',
            'UNIQUE(name)',
            'The name must be unique'
        ),
    ]
