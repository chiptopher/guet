from os.path import isdir
from shutil import rmtree
from typing import List

from guet.steps.action import Action
from guet.util import project_root


class RemoveLocal(Action):
    def execute(self, args: List[str]):
        if isdir(project_root().joinpath('.guet')):
            rmtree(project_root().joinpath('.guet'))
            print('guet tracking removed from this repository')
        else:
            print('No local guet configurations for this project')
