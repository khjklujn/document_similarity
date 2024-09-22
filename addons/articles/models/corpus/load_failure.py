import logging

from odoo import fields, models

_logger = logging.getLogger(__file__)


class LoadFailure(models.Model):
    _name = 'articles.load_failure'
    _description = 'Load Failures'
    _order = 'name'

    name = fields.Char(
        required=True,
        index=True,
        readonly=True
    )

    unique_id = fields.Char(
        required=True,
        index=True,
        readonly=True,
        old_name='sha512'
    )

    category = fields.Char(
        required=True,
        index=True,
        readonly=True
    )

    reason = fields.Text(
        required=True,
        index=True,
        readonly=True
    )

    _sql_constraints = [
        (
            'unique_id_reason_unique',
            'UNIQUE(unique_id, reason)',
            'The entry must be unique'
        ),
    ]
