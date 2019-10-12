from guet.git.hook_present import hook_present


def any_hooks_present(git_path: str):
    pre_commit_present = hook_present(git_path, 'pre-commit')
    post_commit_present = hook_present(git_path, 'post-commit')
    commit_msg_present = hook_present(git_path, 'commit-msg')

    return pre_commit_present or post_commit_present or commit_msg_present
