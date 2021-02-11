from guet.util import Proxy, project_root

from .committers import Committers


class CommittersProxy(Proxy):
    def loader(self):
        try:
            root = project_root()
        except FileNotFoundError:
            root = None
        return Committers(path_to_project_root=root)
