from pathlib import Path
from typing import List

from guet.git._create_strategy import CreateStrategy
from guet.git._file_name_strategy import FileNameStrategy
from guet.git.errors import NotGuetHookError
from guet.git.hook import Hook


class HookLoader:
    def __init__(self, path_to_repository: Path, file_name: FileNameStrategy, create: CreateStrategy):
        self.create = create
        self.file_name = file_name
        self.path_to_repository = path_to_repository

    def apply(self, hook_name: str, hooks: List[Hook]):
        hook_path = self.path_to_repository.joinpath('hooks').joinpath(self.file_name.apply(hook_name))
        try:
            hooks.append(Hook(hook_path, create=self.create.apply()))
        except FileNotFoundError:
            pass
        except NotGuetHookError:
            pass
