import ssl
import time
import xmlrpc.client


class Odoo:
    def __init__(self, url: str, user: str, password: str, database: str):
        self._password = password
        self._database = database

        connection = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/common'.format(url),
            context=ssl._create_unverified_context()
        )

        self._uid = connection.authenticate(
            database,
            user,
            password,
            {}
        )
        self._connection = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/object'.format(url),
            context=ssl._create_unverified_context()
        )

    def close(self):
        pass

    def commit(self):
        pass

    def create(self, table: str, values: list):
        retry = 0
        while retry < 5:
            try:
                return self.connection.execute_kw(
                    self.database,
                    self.uid,
                    self.password,
                    table,
                    'create',
                    values
                )
            except Exception:
                retry += 1
                time.sleep(5)
                if retry > 4:
                    raise

    def rollback(self):
        pass

    def search(self, table: str, filters: list, **kwargs):
        retry = 0
        while retry < 5:
            try:
                return self.connection.execute_kw(
                    self.database,
                    self.uid,
                    self.password,
                    table,
                    'search',
                    filters,
                    kwargs
                )
            except Exception:
                retry += 1
                time.sleep(5)
                if retry > 4:
                    raise

    def search_with_active(self, table: str, filters: list, **kwargs):
        exists = self.search(table, filters)
        filters[0].append(['active', '=', False])
        exists += self.search(table, filters, **kwargs)
        return exists

    def search_read(self, table, filters, fields, **kwargs):
        iRetry = 0
        while iRetry < 5:
            try:
                return self.connection.execute_kw(
                    self.database,
                    self.uid,
                    self.password,
                    table,
                    'search_read',
                    filters,
                    fields,
                    **kwargs
                )
            except Exception:
                iRetry += 1
                time.sleep(5)
                if iRetry > 4:
                    raise

    def search_read_with_active(self, table: str, filters: list, fields: dict, **kwargs):
        lExists = self.search_read(table, filters, fields)
        filters[0].append(['active', '=', False])
        lExists += self.search_read(table, filters, fields, **kwargs)
        return lExists

    def upsert_single(self, table: str, filters: list, values: dict):
        exists = self.search_read(
            table,
            filters,
            {
                'fields': list(values.keys())
            }
        )

        if exists:
            row_id = exists[0]['id']
            del exists[0]['id']
            if exists[0] != values:
                self.write(
                    table,
                    [[row_id], values]
                )
        else:
            row_id = self.create(
                table,
                [values]
            )
        return row_id

    def upsert_single_with_active(self, table: str, filters: list, values: dict):
        exists = self.search_read_with_active(
            table,
            filters,
            {
                'fields': list(values.keys())
            }
        )

        if exists:
            row_id = exists[0]['id']
            del exists[0]['id']
            if exists[0] != values:
                self.write(
                    table,
                    [[row_id], values]
                )
        else:
            row_id = self.create(
                table,
                [values]
            )
        return row_id

    def upsert_many(self, table: str, **records):
        retry = 0
        while retry < 5:
            return self.connection.execute_kw(
                self.database,
                self.uid,
                self.password,
                table,
                'upsert',
                tuple(),
                records
            )

    def write(self, table: str, values: list):
        retry = 0
        while retry < 5:
            try:
                return self.connection.execute_kw(
                    self.database,
                    self.uid,
                    self.password,
                    table,
                    'write',
                    values
                )
            except Exception:
                retry += 1
                time.sleep(5)
                if retry > 4:
                    raise

    @property
    def connection(self):
        return self._connection

    @property
    def database(self):
        return self._database

    @property
    def password(self):
        return self._password

    @property
    def uid(self):
        return self._uid
