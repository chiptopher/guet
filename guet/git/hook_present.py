from os.path import isfile, join


def hook_present(path: str, hook_name: str):
    return isfile(join(path, hook_name))
