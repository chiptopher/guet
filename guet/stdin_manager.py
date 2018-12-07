

class StdinManager:

    _instance = None

    def __init__(self):
        if StdinManager._instance is None:
            StdinManager._instance = self
            import sys
            self._stdin = sys.__stdin__

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            StdinManager()
        return cls._instance

    def get_stdin(self):
        return self._stdin

    def set_stdin(self, stdin):
        self._stdin = stdin
