from guet.steps.check.check import Check
from guet.git.git import Git
from guet.git.errors import NoGitPresentError

GIT_REQUIRED_MESSAGE = "Git not installed in this directory."


class GitRequiredCheck(Check):

    def __init__(self, git: Git):
        super().__init__("Git not installed in this directory.")
        self.git = git

    def should_stop(self, args):
        try:
            # TODO because the times this is called, a GitProxy is going
            #      to be used, we can hack it a bit. The initialization
            #      sequence in the GitProxy will raise a FileNotFoundError
            #      if it can't find the git folder. This should be removed
            #      as a part of the Git refactor.
            self.git.hooks_present()
            return False
        except FileNotFoundError:
            return True
