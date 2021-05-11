from os import getcwd
from pathlib import Path
from typing import List

from guet.git import Git
from guet.steps.preparation import Preparation


class ChangeHooksFolder(Preparation):
    def __init__(self, git: Git):
        super().__init__()
        self._git = git

    def prepare(self, args: List[str]):
        if '--location' in args:
            location_flag_position = args.index('--location')
            if (location_flag_position + 1) >= len(args):
                print(('No argument following hook location flag. '
                       'Default hooks path used instead.'))
            else:
                self._change_hooks_directory(args)

    def _change_hooks_directory(self, args: List[str]):
        location_flag_position = args.index('--location')
        maybe_path = Path(getcwd(), args[location_flag_position + 1])
        if maybe_path.is_dir():
            self._git.set_hooks_destination(maybe_path)
        else:
            print((f'Not a folder: {maybe_path.absolute()}'
                   '. Default hooks path used instead.'))
