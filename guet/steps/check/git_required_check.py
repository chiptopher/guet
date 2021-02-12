from guet.git.git import Git
from guet.steps.check.check import Check

GIT_REQUIRED_MESSAGE = "Git not installed in this directory."


class GitRequiredCheck(Check):

    def __init__(self, git: Git):
        super().__init__(GIT_REQUIRED_MESSAGE)
        self.git = git

    def should_stop(self, args):
        try:
            # This depends on GitProxy loading it's Git internally, causing the FileNotFoundError.
            self.git.hooks_present()
            return False
        except FileNotFoundError:
            return True
