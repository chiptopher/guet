from typing import List

from guet.commands.get.committer_printing_strategy import CommitterPrintingStrategy


class ShortCommittersListStrategy(CommitterPrintingStrategy):
    def apply(self, args: List[str], _unused):
        initials = [committer.initials for committer in self.committers]
        print(', '.join(initials))
