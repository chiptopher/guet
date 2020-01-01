from typing import List

from guet.commands.strategy import CommandStrategy
from guet.settings.settings import Settings


class HelpMessageBuilder:

    def __init__(self, usage: str, description: str):
        self._usage = usage
        self._description = description
        self._explanation = None

    def explanation(self, explanation: str):
        self._explanation = explanation
        return self

    def build(self) -> str:
        message = f'usage: {self._usage}\n\n{self._description}'
        if self._explanation is not None:
            message += f'\n\n{self._explanation}'
        return f'{message}\n'


class HelpMessageStrategy(CommandStrategy):
    def __init__(self, help_message: str):
        self.help_message = help_message

    def apply(self):
        print(self.help_message)
