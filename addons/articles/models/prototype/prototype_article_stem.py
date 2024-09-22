import logging

from odoo import fields, models

_logger = logging.getLogger(__file__)


class PrototypeArticleStem(models.Model):
    _name = 'articles.prototype_article_stem'
    _description = 'Characterizing Word Distribution for the Prototype Article'
    _order = 'occurrences desc'

    prototype_article_id = fields.Many2one(
        'articles.prototype_article',
        required=True,
        index=True,
        readonly=True,
        ondelete='cascade'
    )

    stem_id = fields.Many2one(
        'articles.stem',
        required=True,
        index=True,
        readonly=True
    )

    occurrences = fields.Integer(
        required=True,
        readonly=True
    )

    nouniness = fields.Float(
        digits=(19, 5),
        required=True,
        readonly=True
    )

    verbiness = fields.Float(
        digits=(19, 5),
        required=True,
        readonly=True
    )

    _sql_constraints = [
        (
            'stem_id_prototype_article_id_unique',
            'UNIQUE(stem_id, prototype_article_id)',
            'The entry must be unique'
        ),
    ]
