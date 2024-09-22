import connector

from .session import Session


class Grobid(Session):
    def __enter__(self):
        self._session = connector.Grobid(  # type: ignore
            self.config.grobid_url
        )
        return self
