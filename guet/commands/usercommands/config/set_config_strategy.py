from typing import List

from guet.commands.strategies.strategy import CommandStrategy
from guet.settings.get_settings import get_settings
from guet.settings.set_settings import set_settings
from guet.context.context import Context
from guet.settings.settings import Settings


def _only_args_starting_with_double_dash(args: List) -> List[str]:
    return [arg for arg in args if arg.startswith('--')]


def _remove_double_dash(key: str) -> str:
    return key.replace('--', '')


def _append_key_and_value_to_config(config: Settings, key_and_value: List):
    for key_value in key_and_value:
        try:
            config.set(key_value[0], key_value[1])
        except KeyError:
            print(f'Cannot set \"{key_value[0]}\", not valid configuration.\n')
            exit(1)


class SetConfigStrategy(CommandStrategy):

    def __init__(self, args: List[str], context: Context):
        self._args = args
        self.context = context

    def apply(self):
        config = get_settings()
        key_and_value = self._separate_key_and_value()
        _append_key_and_value_to_config(config, key_and_value)
        set_settings(config)

    def _separate_key_and_value(self) -> List:
        key_and_value = []
        for arg in _only_args_starting_with_double_dash(self._args):
            key, value = arg.split('=')
            key_and_value.append((_remove_double_dash(key), value))
        return key_and_value
