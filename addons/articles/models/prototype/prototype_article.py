import logging

from odoo import fields, models

_logger = logging.getLogger(__file__)


class PrototypeArticle(models.Model):
    _name = 'articles.prototype_article'
    _description = 'Prototype Articles'
    _order = 'name'

    topic_id = fields.Many2one(
        'articles.topic',
        required=True,
        index=True
    )

    name = fields.Char(
        required=True,
        index=True
    )

    unique_id = fields.Char(
        required=True,
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

    prototype_article_stem_ids = fields.One2many(
        'articles.prototype_article_stem',
        'prototype_article_id',
        readonly=True,
        string='Stems'
    )

    prototype_article_corpus_article_ids = fields.One2many(
        'articles.prototype_article_corpus_article',
        'prototype_article_id',
        readonly=True,
        string='Corpus Articles'
    )

    _sql_constraints = [
        (
            'topic_id_name_unique',
            'UNIQUE(topic_id, name)',
            'The name must be unique'
        ),
        (
            'topic_id_unique_id_unique',
            'UNIQUE(topic_id, unique_id)',
            'The unique id must be unique'
        ),
    ]
