import util


class Session:
    def __init__(self, config: util.Config):
        self._config = config
        self._session = None

    def __exit__(self, type, value, traceback):
        self.session.close()

    @property
    def config(self):
        return self._config

    @property
    def session(self):
        return self._session
