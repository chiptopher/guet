from guet.hooks.commit_msg import commit_msg


def manage(hook: str):
    if hook.endswith('commit-msg'):
        commit_msg()
