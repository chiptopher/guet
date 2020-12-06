from guet.util import Proxy

from .committers import Committers


class CommittersProxy(Proxy):
    def loader(self):
        return Committers()
