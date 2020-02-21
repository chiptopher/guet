class FileNameStrategy:
    def apply(self, base_name: str) -> str:
        raise NotImplementedError()


class AlongsideFileNameStrategy(FileNameStrategy):
    def apply(self, base_name: str):
        return base_name + '-guet'


class BaseFileNameStrategy(FileNameStrategy):
    def apply(self, base_name: str) -> str:
        return base_name
