from typing import List

from guet.commands.strategy_command import CommandStrategy, StrategyCommand


class _GetStrategy:
    def __init__(self, list_flag=False):
        self.list_flag = list_flag

    def apply(self, args: List[str]):
        raise NotImplementedError


class GetCommand(StrategyCommand):
    def __init__(self, args: List[str], settings, command_strategy: CommandStrategy, args_needed=True):
        super().__init__(args, settings, command_strategy, args_needed=args_needed)

    @classmethod
    def help_short(cls):
        return ''

    def help(self):
        return """usage: guet get <identifier>\n\nValid Identifier\n\n\tcurrent - lists currently set committers\n\tcomitters - lists all committers"""
