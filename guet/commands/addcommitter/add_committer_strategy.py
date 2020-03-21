from guet.commands.strategy import CommandStrategy
from guet.config.committer import Committer
from guet.config.committers import Committers


class AddCommitterStrategy(CommandStrategy):
    def __init__(self, initials: str, name: str, email: str, committers: Committers):
        super().__init__()
        self._name = name
        self._email = email
        self._initials = initials
        self._committers = committers

    def apply(self):
        self._committers.add(Committer(name=self._name, email=self._email, initials=self._initials))
