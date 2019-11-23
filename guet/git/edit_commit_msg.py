from os.path import join
from typing import List


def edit_commit_msg(git_path: str, message: List[str]) -> None:
    file = open(join(git_path, 'COMMIT_EDITMSG'), 'w')
    file.writelines(message)
    file.close()
