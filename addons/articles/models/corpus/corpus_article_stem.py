import logging

from odoo import fields, models

_logger = logging.getLogger(__file__)


class CorpusArticleStem(models.Model):
    _name = 'articles.corpus_article_stem'
    _description = 'Characterizing Word Distribution for the Corpus Article'
    _order = 'occurrences desc'

    corpus_article_id = fields.Many2one(
        'articles.corpus_article',
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

    weight = fields.Float(
        related='stem_id.weight'
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
            'corpus_article_id_stem_id_unique',
            'UNIQUE(corpus_article_id, stem_id)',
            'The entry must be unique'
        ),
    ]
