from guet.commands.scriptcommands.commitmsg.commitmsg_factory import CommitMsgFactory
from guet.util.errors import log_on_error

from guet.config.get_config import get_config


@log_on_error
def commit_msg():
    factory = CommitMsgFactory()
    command = factory.build([], get_config())
    command.execute()
