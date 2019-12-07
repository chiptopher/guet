from guet.commands.command import Command
from guet.config.get_current_committers import get_current_committers
from guet.config.committer import Committer
from guet.config.get_committers import get_committers


class GetCommand(Command):
    def execute_hook(self):
        identifier = self.args[0]
        if identifier == 'current':
            _print_current_committers()
        elif identifier == 'committers':
            _print_all_committers()
        else:
            _print_invalid_identifier_message(self.args[0])

    @classmethod
    def help_short(cls):
        return ''

    def help(self):
        return """usage: guet get <identifier>\n\nValid Identifier\n\n\tcurrent - lists currently set committers\n\tcomitters - lists all committers"""


def _print_current_committers():
    current = get_current_committers()
    print('Currently set committers')
    for committer in current:
        print(_format_committer(committer))


def _print_all_committers():
    print('All committers')
    for committer in get_committers():
        print(_format_committer(committer))


def _print_invalid_identifier_message(identifier: str):
    print(f'Invalid identifier <{identifier}>')


def _format_committer(committer: Committer):
    return f'{committer.initials} - {committer.name} <{committer.email}>'
