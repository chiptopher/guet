from os.path import join
from typing import List


def edit_commit_msg(git_path: str, message: List[str]) -> None:
    f = open(join(git_path, 'COMMIT_EDITMSG'), 'w')
    f.writelines(message)
    f.close()
