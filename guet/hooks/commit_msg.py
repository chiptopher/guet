from guet.commands.scriptcommands.commitmsg.commitmsg_factory import CommitMsgFactory
from guet.util.errors import log_on_error

from guet.settings.get_settings import get_settings


@log_on_error
def commit_msg():
    factory = CommitMsgFactory()
    command = factory.build([], get_settings())
    command.execute()
