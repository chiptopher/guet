from pathlib import Path
from shutil import rmtree
from typing import List

from guet.config import CONFIGURATION_DIRECTORY
from guet.steps.action import Action


class RemoveGlobal(Action):
    def execute(self, args: List[str]):
        if any(arg in ('-g', '--global') for arg in args):
            configuration_dir = Path(CONFIGURATION_DIRECTORY)
            rmtree(configuration_dir)
            print('Bye!')
