import logging

from odoo import fields, models

_logger = logging.getLogger(__file__)


class Word(models.Model):
    _name = 'articles.word'
    _description = 'Words'
    _order = 'name'

    stem_id = fields.Many2one(
        'articles.stem',
        required=True,
        index=True,
        readonly=True
    )

    name = fields.Char(
        required=True,
        index=True,
        readonly=True
    )

    active = fields.Boolean(
        required=True,
        default=True
    )

    _sql_constraints = [
        (
            'name_unique',
            'UNIQUE(name)',
            'The name must be unique'
        ),
    ]
