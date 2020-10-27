from pathlib import Path
from os import mkdir
from typing import List
from guet.steps.preparation.preapration import Preparation
from guet.config import CONFIGURATION_DIRECTORY
from guet.files import FileSystem, File
from guet import constants


class InitializePreparation(Preparation):
    def __init__(self, file_system: FileSystem):
        super().__init__()
        self._file_system = file_system

    def prepare(self, args: List[str]):
        self._create_configuration_folder()

        configuration_dir = Path(CONFIGURATION_DIRECTORY)

        self._create_empty_file(configuration_dir.joinpath(constants.COMMITTER_NAMES))
        self._create_empty_file(configuration_dir.joinpath(constants.COMMITTERS))
        self._create_empty_file(configuration_dir.joinpath(constants.COMMITTERS_SET))
        self._create_empty_file(configuration_dir.joinpath(constants.ERRORS))

        self._file_system.save_all()

    def _create_empty_file(self, path: Path) -> None:
        self._file_system.get(path).read()

    def _create_configuration_folder(self) -> None:
        mkdir(CONFIGURATION_DIRECTORY)
