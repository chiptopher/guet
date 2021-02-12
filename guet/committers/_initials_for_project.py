from pathlib import Path
from typing import List

from guet.util import current_millis

from ._committers_set import all_committers_set

_TWENTY_FOUR_HOURS_IN_MILLISECONDS = 86400000


def _new_set_required(current_project_set) -> bool:
    reset_time = int(current_project_set.set_time) + _TWENTY_FOUR_HOURS_IN_MILLISECONDS
    return reset_time < current_millis()


def initials_for_project(project_root: Path) -> List[str]:
    try:
        current_project_set = next(
            c for c in all_committers_set() if c.path == project_root)

        if _new_set_required(current_project_set):
            return []
        else:
            return current_project_set.initials

    except StopIteration:
        return []
