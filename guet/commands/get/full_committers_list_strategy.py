from typing import List

from guet.commands.get.committer_printing_strategy import CommitterPrintingStrategy


class FullCommittersListStrategy(CommitterPrintingStrategy):
    def apply(self, args: List[str], _unused):
        for committer in self.committers:
            print(f'{committer.initials} - {committer.name} <{committer.email}>')
