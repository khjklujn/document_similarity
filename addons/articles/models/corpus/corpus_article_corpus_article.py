import logging

from odoo import fields, models

_logger = logging.getLogger(__file__)


class CorpusArticleCorpusArticle(models.Model):
    _name = 'articles.corpus_article_corpus_article'
    _description = 'Corpus Article Corpus Article'
    _order = 'distance desc'

    prototype_article_id = fields.Many2one(
        'articles.corpus_article',
        required=True,
        index=True,
        readonly=True
    )

    corpus_article_id = fields.Many2one(
        'articles.corpus_article',
        required=True,
        index=True,
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

    divergence = fields.Float(
        digits=(6, 5),
        index=True,
        readonly=True
    )

    alpha = fields.Float(
        digits=(6, 5),
        index=True,
        readonly=True
    )

    beta = fields.Float(
        digits=(6, 5),
        index=True,
        readonly=True
    )

    _sql_constraints = [
        (
            'prototype_article_corpus_article_unique',
            'UNIQUE(prototype_article_id, corpus_article_id)',
            'The entry must be unique'
        ),
    ]
