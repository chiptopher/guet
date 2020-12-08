import sys

from guet.util.errors import log_on_error
from guet.util import get_command_key
from guet.context.context import Context
from guet.commands import CommandMap
from guet.commands.add import AddCommandFactory
from guet.commands.get import GetCommandFactory
from guet.commands.help import HelpCommandFactory
from guet.commands.init import InitCommandFactory
from guet.commands.set import SetCommittersCommand
from guet.committers import CommittersProxy
from guet.files import FileSystem
from guet.git import GitProxy

file_system = FileSystem()
committers = CommittersProxy()
git = GitProxy()
context = Context(None, file_system=file_system, git=git, committers=committers)


@log_on_error
def main():
    command_map = CommandMap()
    command_map.add_command('help', HelpCommandFactory(command_map, file_system), 'Display guet usage')
    command_map.add_command('init', InitCommandFactory(GitProxy(), file_system), 'Start guet tracking in the current repository')
    command_map.add_command('add', AddCommandFactory(file_system, committers), 'Add committer for tracking')
    command_map.add_command('get', GetCommandFactory(file_system, committers), 'List information about committers')
    command_map.add_command('set', SetCommittersCommand(file_system, committers, context), 'Set committers for current repository')

    command = command_map.get_command(get_command_key(sys.argv[1:])).build()
    command.play(sys.argv[2:])
