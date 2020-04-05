from guet.commands.scriptcommands.precommit.precommit_factory import PreCommitFactory
from guet.config.get_config import get_config
from guet.util.errors import log_on_error


@log_on_error
def pre_commit():
    factory = PreCommitFactory()
    command = factory.build([], get_config())
    command.execute()
