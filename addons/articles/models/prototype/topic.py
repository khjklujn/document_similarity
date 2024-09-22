import logging

from odoo import fields, models

_logger = logging.getLogger(__file__)


class Topic(models.Model):
    _name = 'articles.topic'
    _description = 'Topics'
    _order = 'name'

    name = fields.Char(
        required=True,
        index=True
    )

    active = fields.Boolean(
        required=True,
        default=True
    )

    prototype_article_ids = fields.One2many(
        'articles.prototype_article',
        'topic_id',
        readonly=True,
        string='Prototype Articles'
    )

    _sql_constraints = [
        (
            'name_unique',
            'UNIQUE(name)',
            'The name must be unique'
        ),
    ]
