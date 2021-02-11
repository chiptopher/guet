from os import mkdir
from os.path import isdir
from pathlib import Path
from typing import List

from guet.steps.preparation.preapration import Preparation


class LocalPreparation(Preparation):
    def __init__(self, project_root: Path):
        super().__init__()
        self._project_root = project_root

    def prepare(self, args: List[str]):
        local_guet_directory = self._project_root.joinpath('.guet')
        if not isdir(local_guet_directory):
            mkdir(local_guet_directory)
