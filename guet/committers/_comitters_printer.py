from typing import List

from guet.committers.committer import Committer

from ._initials_formatter import InitialsFormatter
from ._initials_name_email_printer import InitialsNameEmailPrintFormatter


class CommittersPrinter:
    def __init__(self, *, initials_only: bool):
        self.initials_only = initials_only

    def print(self, committers: List[Committer]):
        if self.initials_only:
            self._initials_print(committers)
        else:
            self._pretty_print(committers)

    def _initials_print(self, committers: List[Committer]):
        print(str(InitialsFormatter(committers)))

    def _pretty_print(self, committers: List[Committer]):
        for committer in committers:
            print(str(InitialsNameEmailPrintFormatter(committer)))
