from pathlib import Path
from typing import List

from guet.util import current_millis

from ._committers_set import all_committers_set

_TWENTY_FOUR_HOURS_IN_MILLISECONDS = 86400000


def initials_for_project(project_root: Path) -> List[str]:
    try:
        current_project_set = next(
            c for c in all_committers_set() if c.path == project_root)
        if int(current_project_set.set_time) + _TWENTY_FOUR_HOURS_IN_MILLISECONDS < current_millis():
            return []
        else:
            return current_project_set.initials

    except StopIteration:
        return []
