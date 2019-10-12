from enum import Enum
from os import chmod, stat

from guet.git._create_hook_post_commit_strategy import _PostCommitStrategy
from guet.git._create_hook_pre_commit_strategy import _PreCommitStrategy
from guet.git._create_hook_commit_msg_strategy import _CommitMsgStrategy
from guet.git._hook_mode import HookMode


class Hooks(Enum):
    PRE_COMMIT = _PreCommitStrategy
    COMMIT_MSG = _CommitMsgStrategy
    POST_COMMIT = _PostCommitStrategy


def create_hook(hook_folder_path: str, hook: Hooks, create_mode: HookMode):
    hook_strategy = hook.value(hook_folder_path, create_mode)
    final_hook_path = hook_strategy.final_hook_path()
    f = open(final_hook_path, 'w')
    f.writelines(hook_strategy.file_lines())
    f.close()

    st = stat(final_hook_path)
    chmod(final_hook_path, st.st_mode | 0o111)
