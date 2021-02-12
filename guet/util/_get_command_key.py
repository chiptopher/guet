from typing import List


def get_command_key(args: List[str]) -> str:
    if len(_strip_flags(args)) == 0:
        return 'help'
    else:
        return args[0]


def _strip_flags(args: List[str]) -> List[str]:
    return [arg for arg in args if not arg.startswith('-')]
