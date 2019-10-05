
from guet.git.hook_present import hook_present


def any_hooks_present(git_path: str):
    pre_commit_present = hook_present(git_path, 'pre-commit')
    post_commit_present = hook_present(git_path, 'post-commit')
    commit_msg_present = hook_present(git_path, 'commit-msg')

    return pre_commit_present and post_commit_present and commit_msg_present
