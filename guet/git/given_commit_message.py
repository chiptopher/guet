from os.path import join


def given_commit_message(path_to_git: str):
    file = open(join(path_to_git, 'COMMIT_EDITMSG'), 'r')
    lines = file.readlines()
    file.close()
    return lines
