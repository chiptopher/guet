from typing import List

from guet.committers import Committers2 as Committers
from guet.committers.committer import Committer
from guet.files import FileSystem
from guet.util import project_root

from ._initials_for_project import initials_for_project
from ._set_current_committers import set_current_committers


class CurrentCommittersObserver:
    def on_new_committers(self, committers: List[Committer]):
        pass


class CurrentCommitters:
    def __init__(self, file_system: FileSystem, committers: Committers):
        self.committers = committers
        self.file_system = file_system
        self.observers = []

    def get(self) -> List[Committer]:
        project_initials = initials_for_project(project_root())
        committers = []
        for initials in project_initials:
            committers.append(self.committers.by_initials(initials))
        return committers

    def set(self, committers: List[Committer]):
        set_current_committers(committers, project_root())
        for observer in self.observers:
            observer.on_new_committers(committers)

    def register_observer(self, observer: CurrentCommittersObserver):
        self.observers.append(observer)
