from os.path import join


def given_commit_message(path_to_git: str):
    f = open(join(path_to_git, 'COMMIT_EDITMSG'), 'r')
    lines = f.readlines()
    f.close()
    return lines
