from typing import List

from guet.committers.committer import Committer

from guet.context.context import Context

from guet.commands.strategies.strategy import CommandStrategy


def _co_authored_lines(committers: List[Committer]) -> List[str]:
    return [f'Co-authored-by: {committer.name} <{committer.email}>' for committer in committers]


def _remove_co_authored_lines(old_message: List[str]) -> List[str]:
    return [line for line in old_message if not line.startswith('Co-authored-by: ')]


def _add_newline_if_necessary(without_co_authored_lines: List[str]) -> List[str]:
    if not without_co_authored_lines[len(without_co_authored_lines) - 1] == '\n':
        without_co_authored_lines.append('\n')
    return without_co_authored_lines


def _append_new_co_authored_lines(old_message: List[str], new_lines: List[str]) -> List[str]:
    without_co_authored_lines = _remove_co_authored_lines(old_message)
    with_newline = _add_newline_if_necessary(without_co_authored_lines)
    return with_newline + new_lines


class CommitMsgStrategy(CommandStrategy):
    def __init__(self, context: Context):
        self.context = context

    def apply(self):
        current = self.context.committers.current()
        if len(current) > 1:
            new_lines = _co_authored_lines(current)
            self.context.git.commit_msg = _append_new_co_authored_lines(self.context.git.commit_msg, new_lines)
