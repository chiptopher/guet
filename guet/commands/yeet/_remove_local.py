from os.path import isdir
from shutil import rmtree
from typing import List

from guet.files import FileSystem
from guet.git import Git, all_guet_hooks
from guet.steps.action import Action
from guet.util import project_root


class RemoveLocal(Action):
    def __init__(self, git: Git, file_system: FileSystem):
        super().__init__()
        self.git = git
        self.file_system = file_system

    def execute(self, args: List[str]):
        for hook in all_guet_hooks(self.file_system):
            hook.delete()
        if isdir(project_root().joinpath('.guet')):
            rmtree(project_root().joinpath('.guet'))
            print('guet tracking removed from this repository')
        else:
            print('No local guet configurations for this project')
