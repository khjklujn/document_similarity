import datetime
import logging

from odoo import api, models

_logger = logging.getLogger(__file__)


class BaseModelExtend(models.AbstractModel):
    _name = 'basemodel.extend'
    _description = 'Upsert Processing'

    def _register_hook(self):

        @api.model
        def upsert(self, key_names=[], records=[]):
            all_column_names = [column for column in records[0]]
            value_column_names = [column for column in records[0] if column not in key_names]

            audit = [
                str(self._uid),
                'now()',
                str(self._uid),
                'now()'
            ]
            values_batched = []
            for record in records:
                values = [self.upsert_escape(record[column]) for column in all_column_names] + audit
                values_batched.append("(%s)" % ', '.join(values))

            values_formated = ',\n'.join(values_batched)

            all_column_names += [
                'create_uid',
                'create_date',
                'write_uid',
                'write_date'
            ]

            insert_columns = '(%s)' % ', '.join(['"%s"' % column for column in all_column_names])
            insert_on_conflict_keys = '(%s)' % ', '.join(['"%s"' % column for column in key_names])
            insert_sets = ',\n                    '.join(['            "%s" = coalesce(excluded."%s", t."%s")' % (column, column, column) for column in value_column_names + ['write_uid', 'write_date']])
            insert_wheres = ' or\n                    '.join(['            t."%s" <> excluded."%s"' % (column, column) for column in value_column_names])

            if insert_wheres:
                insert = """
                    insert into %s as t
                                %s
                    values      %s
                    on conflict %s do update set
                    %s
                    where
                    %s
                """ % (
                    self._table,
                    insert_columns,
                    values_formated,
                    insert_on_conflict_keys,
                    insert_sets,
                    insert_wheres
                )
            else:
                insert = """
                    insert into %s as t
                                %s
                    values      %s
                    on conflict %s do nothing
                """ % (
                    self._table,
                    insert_columns,
                    values_formated,
                    insert_on_conflict_keys
                )

            _logger.debug(insert)

            self._cr.execute(insert)

            return True

        models.BaseModel.upsert = upsert

        def upsert_escape(self, value):
            if value == 'null':
                return value
            elif isinstance(value, str):
                return "'%s'" % value.replace("'", "''")
            elif isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                return "'%s'" % value
            else:
                return str(value)

        models.BaseModel.upsert_escape = upsert_escape

        return super(BaseModelExtend, self)._register_hook()


