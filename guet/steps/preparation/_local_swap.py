from os.path import isdir
from typing import List

from guet.committers import Committers2 as Committers
from guet.steps.preparation.preapration import Preparation
from guet.util import project_root


class SwapToLocal(Preparation):
    def __init__(self, committers: Committers):
        super().__init__()
        self.committers = committers

    def prepare(self, args: List[str]):
        try:
            local_guet_directory = project_root().joinpath('.guet')
            if isdir(local_guet_directory):
                self.committers.to_local()
        except FileNotFoundError:
            pass
