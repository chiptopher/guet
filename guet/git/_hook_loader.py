from pathlib import Path
from typing import List

from guet.git._create_strategy import CreateStrategy
from guet.git._file_name_strategy import FileNameStrategy
from guet.git.errors import NotGuetHookError
from guet.git.hook import Hook


class HookLoader:
    def __init__(self,
                 hooks_dir: Path,
                 file_name: FileNameStrategy,
                 create: CreateStrategy):
        self.create = create
        self.file_name = file_name
        self._hooks_directory: Path = hooks_dir

    def _create_hooks_directory_if_not_present(self):
        if not self._hooks_directory.is_dir():
            self._hooks_directory.mkdir()
            print('No hooks directory found, creating one.')

    def apply(self, hook_name: str, hooks: List[Hook]):
        self._create_hooks_directory_if_not_present()
        hook_path = self._hooks_directory.joinpath(self.file_name.apply(hook_name))
        try:
            hooks.append(Hook(hook_path, create=self.create.apply()))
        except FileNotFoundError:
            pass
        except NotGuetHookError:
            pass
