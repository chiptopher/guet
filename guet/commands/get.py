from guet.commands.command import Command
from guet.config.get_current_committers import get_current_committers
from guet.config.committer import Committer


class GetCommand(Command):
    def execute_hook(self):
        if self.args[0] == 'current':
            _print_current_committers()
        else:
            _print_invalid_identifier_message(self.args[0])

    @classmethod
    def help_short(cls):
        return ''

    def help(self):
        return """usage: guet get <identifier>\n\nValid Identifier\n\n\tcurrent - gets the currently set committers"""


def _print_current_committers():
    current = get_current_committers()
    print('Currently set committers')
    for committer in current:
        print(_format_committer(committer))


def _print_invalid_identifier_message(identifier: str):
    print(f'Invalid identifier <{identifier}>')


def _format_committer(committer: Committer):
    return f'{committer.initials} - {committer.name} <{committer.email}>'
