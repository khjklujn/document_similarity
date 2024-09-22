import logging

from odoo import fields, models

_logger = logging.getLogger(__file__)


class Year(models.Model):
    _name = 'articles.year'
    _description = 'Years'
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

    corpus_article_ids = fields.One2many(
        'articles.corpus_article',
        'year_id',
        string='Corpus Articles',
        readonly=True
    )

    _sql_constraints = [
        (
            'name_unique',
            'UNIQUE(name)',
            'The name must be unique'
        ),
    ]
