from guet.committers._add_committer import add_committer
from guet.committers.committer import Committer


class GlobalCommitter(Committer):
    def save(self):
        add_committer(self.initials, self.name, self.email)
