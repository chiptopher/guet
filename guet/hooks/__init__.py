from guet.hooks.commit_msg import commit_msg as _commit_msg
from guet.hooks.post_commit import post_commit as _post_commit
from guet.hooks.pre_commit import pre_commit as _pre_commit

_HOOK_MAP = {
    '.git/hooks/commit-msg': _commit_msg,
    '.git/hooks/commit-msg-guet': _commit_msg,
    '.git/hooks/pre-commit': _pre_commit,
    '.git/hooks/pre-commit-guet': _pre_commit,
    '.git/hooks/post-commit': _post_commit,
    '.git/hooks/post-commit-guet': _post_commit
}


def manage(hook_filepath: str, *, hook_map=_HOOK_MAP):
    try:
        hook_method = hook_map[hook_filepath]
        hook_method()
    except KeyError:
        pass
