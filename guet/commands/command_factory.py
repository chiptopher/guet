from typing import List

from guet.settings.settings import Settings


class CommandFactoryMethod:

    def short_help_message(self):
        raise NotImplementedError

    def build(self, args: List[str], settings: Settings):
        raise NotImplementedError
