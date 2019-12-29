from typing import List

from guet.commands.command import Command
from guet.settings.settings import Settings


class ArgSettingCommand(Command):
    @classmethod
    def get_short_help_message(cls):
        return cls.help_short()

    def __init__(self, args: List[str], settings: Settings, args_needed: bool = True):
        self.args_needed = args_needed
        self.args = args[1:]
        self.settings = settings

    def execute(self) -> None:
        no_args_given = len(self.args) == 0
        if no_args_given and self.args_needed:
            self._print_help_message()
        else:
            self.execute_hook()

    def execute_hook(self) -> None:
        raise NotImplementedError

    def help(self) -> str:
        raise NotImplementedError

    @classmethod
    def help_short(cls) -> str:
        raise NotImplementedError

    def _print_help_message(self) -> None:
        print(f'{self.help()}\n')
