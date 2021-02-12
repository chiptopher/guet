from guet.util import Proxy, project_root

from .git import Git


class GitProxy(Proxy):

    def loader(self):
        return Git(project_root().joinpath('.git'))
