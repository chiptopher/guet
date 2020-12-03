from pathlib import Path
from os import mkdir
from os.path import isdir
from typing import List
from guet.steps.preparation.preapration import Preparation
from guet.config import CONFIGURATION_DIRECTORY
from guet.files import FileSystem, File
from guet import constants
from guet import __version__


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
        file.read()
        return file

    def _create_configuration_folder(self) -> None:
        mkdir(CONFIGURATION_DIRECTORY)
