import logging

from odoo import fields, models

_logger = logging.getLogger(__file__)


class ArticleRanking(models.Model):
    _name = 'articles.article_ranking'
    _description = 'Article Ranking'
    _order = 'distance desc'

    corpus_article_id = fields.Many2one(
        'articles.corpus_article',
        required=True,
        index=True,
        readonly=True
    )

    read_status = fields.Selection(
        related='corpus_article_id.read_status',
        store=True,
        index=True
    )

    united_status = fields.Selection(
        related='corpus_article_id.united_status',
        store=True,
        index=True
    )

    training_status = fields.Selection(
        related='corpus_article_id.training_status',
        store=True,
        index=True
    )

    category = fields.Char(
        related='corpus_article_id.category',
        store=True,
        index=True
    )

    tokenized = fields.Html(
        related='corpus_article_id.tokenized',
        readonly=True
    )

    journal_id = fields.Many2one(
        related='corpus_article_id.journal_id',
        store=True,
        index=True,
        readonly=True
    )

    year_id = fields.Many2one(
        related='corpus_article_id.year_id',
        store=True,
        index=True,
        readonly=True
    )

    distance = fields.Float(
        digits=(6, 5),
        index=True,
        readonly=True
    )

    rank = fields.Integer(
        required=True,
        readonly=True
    )

    _sql_constraints = [
        (
            'corpus_article_id_unique',
            'UNIQUE(corpus_article_id)',
            'The entry must be unique'
        ),
    ]
