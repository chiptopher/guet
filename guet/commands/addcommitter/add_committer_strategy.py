from typing import List

from guet.settings.settings import Settings
from guet.commands.strategy import CommandStrategy
from guet.config.add_committer import add_committer


class AddCommitterStrategy(CommandStrategy):
    def __init__(self, initials: str, name: str, email: str):
        super().__init__()
        self._name = name
        self._email = email
        self._initials = initials

    def apply(self, args: List[str], settings: Settings):
        add_committer(self._initials, self._name, self._email)
