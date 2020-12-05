from guet.git import Git
from guet.util import Proxy, project_root


class GitProxy(Proxy):

    def loader(self):
        return Git(project_root().joinpath('.git'))
