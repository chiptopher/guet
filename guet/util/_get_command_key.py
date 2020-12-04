from typing import List


def get_command_key(args: List[str]) -> str:
    if len(args) == 0:
        return 'help'
    else:
        return args[0]

