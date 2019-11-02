from guet.hooks.commit_msg import commit_msg as _commit_msg


def manage(hook: str):
    if hook.endswith('commit-msg'):
        _commit_msg()
