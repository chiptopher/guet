from os import mkdir
from os.path import isdir
from pathlib import Path
from typing import List

from guet.committers import Committers2 as Committers
from guet.files import FileSystem
from guet.steps.preparation import Preparation
from guet.util import project_root


class LocalFilesInitialization(Preparation):
    def __init__(self, file_system: FileSystem, committers: Committers):
        super().__init__()
        self._file_system = file_system
        self.committers = committers

    def prepare(self, args: List[str]):
        if '--local' in args:
            self.committers.to_local()
            config_dir = Path(project_root()).joinpath('.guet')
            if not isdir(config_dir):
                mkdir(config_dir)
                self._create_empty_file(config_dir.joinpath('committers'))
                self._file_system.save_all()

    def _create_empty_file(self, path: Path) -> None:
        file = self._file_system.get(path)
        file.read()
        return file
