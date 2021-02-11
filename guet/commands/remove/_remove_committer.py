from typing import List

from guet.steps.action import Action


class RemoveCommitterAction(Action):
    def __init__(self, committers):
        super().__init__()
        self.committers = committers

    def execute(self, args: List[str]):
        committer = self.committers.by_initials(args[0])
        if not committer:
            print(f'No committer exists with initials {args[0]}')
        else:
            self.committers.remove(committer.initials)
