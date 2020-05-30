from typing import List

from guet.committers.committer import Committer


class CommitterPrintFormatter:

    def __str__(self):
        raise NotImplementedError


class SingleCommitterPrintFormatter(CommitterPrintFormatter):

    def __init__(self, committer: Committer):
        self._committer = committer

    def __str__(self):
        raise NotImplementedError


class MultipleCommitterPrintFormatter(CommitterPrintFormatter):
    def __init__(self, committers: List[Committer]):
        self._committers = committers

    def __str__(self):
        raise NotImplementedError
