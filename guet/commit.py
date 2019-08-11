import datetime

from guet.gateways.gateway import FileGateway, PairSetGateway
from guet.gateways.io import PrintGateway


class PostCommitManager:

    def __init__(self, file_gateway: FileGateway = FileGateway()):
        self._file_gateway = file_gateway

    def manage(self):
        committers = self._file_gateway.get_committers()
        first_committer = committers.pop(0)
        committers.append(first_committer)
        self._file_gateway.set_committers(committers)
        self._file_gateway.set_author_name(committers[0].name)
        self._file_gateway.set_author_email(committers[0].email)


class PreCommitManager:

    def __init__(self, pair_set_gateway: PairSetGateway = PairSetGateway(),
                 print_gateway: PrintGateway = PrintGateway(), exit_method=exit):
        self._print_gateway = print_gateway
        self._pair_set_gateway = pair_set_gateway
        self._exit_method = exit_method

    def manage(self):
        now = round(datetime.datetime.utcnow().timestamp() * 1000)
        twenty_four_hours = 86400000
        twenty_four_hours_ago = now - twenty_four_hours
        if self._pair_set_gateway.get_most_recent_pair_set().set_time < twenty_four_hours_ago:
            self._print_gateway.print("\nYou have not reset pairs in over twenty four hours!\nPlease reset your pairs by using guet set and including your pairs' initials\n")
            self._exit_method(1)
        else:
            self._exit_method(0)
