from dataclasses import asdict, fields
import decimal

import session
import util


class Repository:
    _module = 'articles'

    def __init__(self, Model, unique_fields: list, config: util.Config):
        self._Model = Model
        self._config = config
        self._unique_fields = unique_fields

        table_name = Model.__name__[0].lower()
        for char in Model.__name__[1:]:
            if char.islower():
                table_name += char
            else:
                table_name += f'_{char.lower()}'

        self._table_name = f'{self._module}_{table_name}'

        self._fields = [
            field.name
            for field in fields(Model)
        ]

        self._records: dict = {}
        self._additions: list = []
        self._get_by_unique: dict = {}

    def add(self, model):
        values = ','.join(
            [
                self.quoted(value)
                for key, value in asdict(model).items()
                if key != 'id'
            ] +
            [
                '1',
                'now()',
                '1',
                'now()'
            ]
        )
        self._additions.append(f'({values})')

    def _by_unique(self, name: str):
        def get(value) -> list:
            if not self._get_by_unique.get(name, {}).get(value, None):
                if name not in self._get_by_unique:
                    self._get_by_unique[name] = {}

                fields = ','.join(
                    f'"{field}"'
                    for field in self._fields
                )
                query = f"""
                select
                    {fields}
                from {self.table_name}
                where
                    "{name}" = {self.quoted(value)}
                """
                with session.SLRV2(self._config) as slr_v2:
                    self._get_by_unique[name][value] = [
                        self._Model(
                            **dict(
                                zip(
                                    self._fields,
                                    record
                                )
                            )
                        )
                        for record in slr_v2.session.execute(query).fetchall()
                    ]
            return self._get_by_unique[name][value]
        return get

    def delete(self, id):
        delete = f"""
        delete
        from {self.table_name}
        where
            id = {id}
        """
        with session.SLRV2(self._config) as slr_v2:
            slr_v2.session.execute(delete)
            slr_v2.session.commit()

    def insert(self, model):
        fields = ','.join(
            f'"{field}"'
            for field in self._fields + [
                'create_uid',
                'create_date',
                'write_uid',
                'write_date'
            ]
            if field != 'id'
        )
        values = ','.join(
            [
                self.quoted(value)
                for key, value in asdict(model).items()
                if key != 'id'
            ] +
            [
                '1',
                'now()',
                '1',
                'now()'
            ]
        )
        insert = f"""
        insert into {self.table_name} ({fields})
        values ({values})
        """
        with session.SLRV2(self._config) as slr_v2:
            slr_v2.session.execute(insert)
            slr_v2.session.commit()

    def insert_many(self):
        fields = ','.join(
            f'"{field}"'
            for field in self._fields + [
                'create_uid',
                'create_date',
                'write_uid',
                'write_date'
            ]
            if field != 'id'
        )
        insert = f"""
        insert into {self.table_name} ({fields})
        values {','.join(self._additions)}
        """
        with session.SLRV2(self._config) as slr_v2:
            slr_v2.session.execute(insert)
            slr_v2.session.commit()
        self._additions = []

    def quoted(self, value):
        if (
            isinstance(value, int) or
            isinstance(value, float) or
            isinstance(value, decimal.Decimal)
        ):
            return str(value)
        elif isinstance(value, str):
            return f"""'{value.replace("'", "''")}'""".replace(":", "\\:")
        elif isinstance(value, bool):
            return 'true' if value else 'false'
        elif value is None:
            return 'null'
        else:
            return f"'{value}'"

    def upsert_many(self):
        if not self._additions:
            return

        fields = ','.join(
            f'"{field}"'
            for field in self._fields + [
                'create_uid',
                'create_date',
                'write_uid',
                'write_date'
            ]
            if field != 'id'
        )
        value_column_names = [
            field
            for field in self._fields
            if field not in self._unique_fields + ['id']
        ]
        insert_sets = ','.join(
            [
                f'"{column}" = coalesce(excluded."{column}", t."{column}")'
                for column in value_column_names + ['write_uid', 'write_date']
            ]
        )
        insert_wheres = ' or '.join(
            [
                f't."{column}" <> excluded."{column}"'
                for column in value_column_names
            ]
        )
        insert = f"""
        insert into {self.table_name} as t
            ({fields})
        values
            {','.join(self._additions)}
        on conflict
            ({','.join(f'"{field}"' for field in self._unique_fields)})
        do update set
            {insert_sets}
        where
            {insert_wheres}
        """
        with session.SLRV2(self._config) as slr_v2:
            slr_v2.session.execute(insert)
            slr_v2.session.commit()
        self._additions = []

    def reset(self):
        self._records = {}
        self._get_by_unique = {}

    @property
    def fields(self) -> list:
        return self._fields

    @property
    def records(self) -> dict:
        if not self._records:
            query = f"""
            select
                {','.join(self._fields)}
            from {self._table_name}
            """
            with session.SLRV2(self._config) as slr_v2:
                self._records = {
                    record[self._fields.index('id')]: self._Model(**dict(zip(self._fields, record)))
                    for record in slr_v2.session.execute(query).fetchall()
                }

        return self._records

    @property
    def refresh(self) -> dict:
        self._records = {}
        self._get_by_unique = {}
        return self.records

    @property
    def table_name(self) -> str:
        return self._table_name
