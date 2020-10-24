from guet.steps.check.check import Check
from guet.git.git import Git
from guet.git.errors import NoGitPresentError


class GitRequiredCheck(Check):

    def __init__(self, git_directory):
        super().__init__("Git not installed in this directory.")
        self._git_directory = git_directory

    def should_stop(self, args):
        try:
            Git(self._git_directory)
            return False
        except NoGitPresentError:
            return True
