from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

import util

from .session import Session


class SLRV2(Session):
    def __init__(self, config: util.Config):
        Session.__init__(self, config)

        self._engine = create_engine(self.config.databases['slr_v2'], echo=False, poolclass=NullPool)

    def __enter__(self):
        self._engine.dispose()
        self._session = sessionmaker(bind=self._engine)()
        return self

