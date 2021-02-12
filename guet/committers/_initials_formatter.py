from ._committer_print_formatter import MultipleCommitterPrintFormatter


class InitialsFormatter(MultipleCommitterPrintFormatter):
    def __str__(self):
        return ', '.join([committer.initials for committer in self._committers])
