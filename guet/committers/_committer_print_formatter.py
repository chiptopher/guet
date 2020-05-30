from guet.committers.committer import Committer


class CommitterPrintFormatter:

    def __init__(self, committer: Committer):
        self._committer = committer

    def __str__(self):
        raise NotImplementedError
