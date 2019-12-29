from typing import List

from guet.commands.argsettingcommand import ArgSettingCommand
from guet.config.get_config import get_config
from guet.config.set_config import set_config
from guet.settings.settings import Settings


class ConfigSetCommand(ArgSettingCommand):
    HELP_MESSAGE = 'usage: guet config [--<key>=<value> ...]'
    SHORT_HELP_MESSAGE = 'Change setting values'

    def execute_hook(self) -> None:
        config = get_config()
        key_and_value = self._separate_key_and_value()
        _append_key_and_value_to_config(config, key_and_value)
        set_config(config)

    def help(self) -> str:
        return self.HELP_MESSAGE

    @classmethod
    def help_short(cls) -> str:
        return cls.SHORT_HELP_MESSAGE

    def _separate_key_and_value(self) -> List:
        key_and_value = []
        for arg in _only_args_starting_with_double_dash(self.args):
            split = arg.split('=')
            key_and_value.append((_remove_double_dash(split[0]), split[1]))
        return key_and_value

def _append_key_and_value_to_config(config: Settings, key_and_value: List):
    for key_value in key_and_value:
        try:
            config.set(key_value[0], key_value[1])
        except KeyError:
            print(f'Cannot set \"{key_value[0]}\", not valid configuration.\n')
            exit(1)

def _only_args_starting_with_double_dash(args: List) -> List[str]:
    return [arg for arg in args if arg.startswith('--')]

def _remove_double_dash(key: str) -> str:
    return key.replace('--', '')
