
from guet.gateway import FileGateway


class CommitManager:

    def __init__(self, file_gateway: FileGateway = FileGateway()):
        self._file_gateway = file_gateway

    def manage(self):
        committers = self._file_gateway.get_committers()
        first_committer = committers.pop(0)
        committers.append(first_committer)
        self._file_gateway.set_committers(committers)
        self._file_gateway.set_author_name(committers[0].name)
        self._file_gateway.set_author_email(committers[0].email)
