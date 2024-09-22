import connector

from .session import Session


class Odoo(Session):
    def __enter__(self):
        self._session = connector.Odoo(  # type: ignore
            self.config.odoo_url,
            self.config.odoo_user,
            self.config.odoo_password,
            self.config.odoo_database
        )
        return self
