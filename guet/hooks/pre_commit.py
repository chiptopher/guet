from guet.commands.scriptcommands.precommit.precommit_factory import PreCommitFactory
from guet.settings.get_settings import get_settings
from guet.util.errors import log_on_error


@log_on_error
def pre_commit():
    factory = PreCommitFactory()
    command = factory.build([], get_settings())
    command.execute()
