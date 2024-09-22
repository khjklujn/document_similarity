import logging

from odoo import fields, models

_logger = logging.getLogger(__file__)


class CorpusArticle(models.Model):
    _name = 'articles.corpus_article'
    _description = 'Corpus Articles'
    _order = 'name'

    corpus_id = fields.Many2one(
        'articles.corpus',
        required=True,
        index=True,
        readonly=True
    )

    name = fields.Char(
        required=True,
        index=True
    )

    source_file = fields.Char(
        required=True,
        index=True,
        readonly=True
    )

    unique_id = fields.Char(
        required=True,
        index=True,
        readonly=True
    )

    tokenized = fields.Html(
        required=True,
        readonly=True
    )

    characterized = fields.Html(
        required=True,
        readonly=True
    )

    active = fields.Boolean(
        required=True,
        default=True
    )

    journal_id = fields.Many2one(
        'articles.journal',
        required=True,
        index=True,
        readonly=True
    )

    year_id = fields.Many2one(
        'articles.year',
        required=True,
        index=True,
        readonly=True
    )

    read_status = fields.Selection(
        [
            ('New Prototype', 'New Prototype'),
            ('New Antitype', 'New Antitype'),
            ('Off Topic', 'Off Topic'),
            ('On Topic', 'On Topic'),
            ('Prototype', 'Prototype'),
            ('Antitype', 'Antitype'),
            ('Not Reviewed', 'Not Reviewed'),
        ],
        required=True,
        index=True
    )

    united_status = fields.Selection(
        [
            ('Prototype', 'Prototype'),
            ('Antitype', 'Antitype'),
            ('Not Reviewed', 'Not Reviewed'),
        ],
        index=True
    )

    training_status = fields.Selection(
        [
            ('Off Topic', 'Off Topic'),
            ('On Topic', 'On Topic'),
            ('Not Reviewed', 'Not Reviewed'),
        ],
        required=True,
        index=True,
        default='Not Reviewed'
    )

    category = fields.Char()

    percent_about = fields.Float(
        digits=(3, 2)
    )

    corpus_article_stem_ids = fields.One2many(
        'articles.corpus_article_stem',
        'corpus_article_id',
        readonly=True,
        string='Stems'
    )

    corpus_article_corpus_article_ids = fields.One2many(
        'articles.corpus_article_corpus_article',
        'prototype_article_id',
        readonly=True,
        string='Related Articles'
    )

    prototype_article_corpus_article_ids = fields.One2many(
        'articles.prototype_article_corpus_article',
        'corpus_article_id',
        readonly=True,
        string='Prototype Articles'
    )

    _sql_constraints = [
        (
            'corpus_id_unique_id_unique',
            'UNIQUE(corpus_id, unique_id)',
            'The unique_id must be unique'
        ),
        (
            'corpus_id_source_file_unique',
            'UNIQUE(corpus_id, source_file)',
            'The source file must be unique'
        ),
    ]
