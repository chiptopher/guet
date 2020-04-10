from guet.settings.get_settings import get_settings

from guet.commands.scriptcommands.postcommit.postcommit_factory import PostCommitFactory
from guet.util.errors import log_on_error


@log_on_error
def post_commit():
    factory = PostCommitFactory()
    command = factory.build([], get_settings())
    command.execute()
