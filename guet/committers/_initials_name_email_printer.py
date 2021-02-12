from guet.committers._committer_print_formatter import \
    SingleCommitterPrintFormatter


class InitialsNameEmailPrintFormatter(SingleCommitterPrintFormatter):
    def __str__(self):
        return f'{self._committer.initials} - {self._committer.name} <{self._committer.email}>'
