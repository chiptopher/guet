from typing import List

from guet.settings.settings import Settings


class CommandStrategy:
    def apply(self, args: List[str], settings: Settings):
        raise NotImplementedError
