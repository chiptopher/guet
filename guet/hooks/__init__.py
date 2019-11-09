from guet.hooks.commit_msg import commit_msg as _commit_msg
from guet.hooks.post_commit import post_commit as _post_commit
from guet.hooks.pre_commit import pre_commit as _pre_commit


def manage(hook: str):
    if hook.endswith('commit-msg'):
        _commit_msg()
    elif hook.endswith('pre-commit'):
        _pre_commit()
    elif hook.endswith('post-commit'):
        _post_commit()
