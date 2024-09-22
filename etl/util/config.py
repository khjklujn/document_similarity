import os
import yaml

from . import decrypt


class Config(object):
    def __init__(self, file_name='config.yaml'):
        split_path = os.path.abspath(__file__).split('etl')
        path = os.path.join(split_path[0], 'etl', file_name)
        with open(path, 'r') as file_in:
            self._config = yaml.load(file_in.read(), Loader=yaml.FullLoader)

    @property
    def databases(self):
        ret = {}
        for database_name, database_definition in self._config['databases'].items():
            if database_definition['database']:
                ret[database_name] = '%s://%s:%s@%s/%s' % (database_definition['driver'], database_definition['user'], decrypt.decrypt(database_definition['password']), database_definition['url'], database_definition['database'])
            else:
                ret[database_name] = '%s://%s:%s@%s' % (database_definition['driver'], database_definition['user'], decrypt.decrypt(database_definition['password']), database_definition['url'])
        return ret

    @property
    def grobid_url(self):
        return self._config['grobid']['url']

    @property
    def odoo_database(self):
        return self._config['odoo']['database']

    @property
    def odoo_password(self):
        return decrypt.decrypt(self._config['odoo']['password'])

    @property
    def odoo_url(self):
        return self._config['odoo']['url']

    @property
    def odoo_user(self):
        return self._config['odoo']['user']

    @property
    def source_root(self):
        return self._config['source_root']
