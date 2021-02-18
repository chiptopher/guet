from os import mkdir
from os.path import isdir
from pathlib import Path
from typing import List

from guet import __version__, constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.files import FileSystem
from guet.steps.preparation.preapration import Preparation


class InitializePreparation(Preparation):
    def __init__(self, file_system: FileSystem):
        super().__init__()
        self._file_system = file_system

    def prepare(self, args: List[str]):
        if not isdir(CONFIGURATION_DIRECTORY):
            self._create_configuration_folder()

            configuration_dir = Path(CONFIGURATION_DIRECTORY)

            self._create_empty_file(configuration_dir.joinpath(constants.COMMITTER_NAMES))
            self._create_empty_file(configuration_dir.joinpath(constants.CONFIG))
            self._create_empty_file(configuration_dir.joinpath(constants.COMMITTERS))
            self._create_empty_file(configuration_dir.joinpath(constants.COMMITTERS_SET))
            self._create_empty_file(configuration_dir.joinpath(constants.ERRORS))

            config = self._create_empty_file(Path(configuration_dir.joinpath(constants.CONFIG)))
            config.write([f'{__version__}\n', '\n'])

            self._file_system.save_all()

    def _create_empty_file(self, path: Path) -> None:
        file = self._file_system.get(path)
        file.write([])
        return file

    def _create_configuration_folder(self) -> None:
        mkdir(CONFIGURATION_DIRECTORY)
