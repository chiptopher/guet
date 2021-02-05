from pathlib import Path

from guet.config import CONFIGURATION_DIRECTORY
from guet.files import File


class _FileMap(dict):
    def __missing__(self, key: Path):
        self[key] = File(key)
        return self[key]


class FileSystem:
    def __init__(self):
        self._file_cache: _FileMap = _FileMap()

    def get(self, path: Path) -> File:
        return self._file_cache[path]

    def save_all(self):
        for path in self._file_cache:
            file = self._file_cache[path]
            file.save()

    @staticmethod
    def config_directory() -> Path:
        return Path(CONFIGURATION_DIRECTORY)
