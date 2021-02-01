from typing import List


def add_command_help_if_invalid_command_given(args: List[str]) -> List[str]:
    if args[0].startswith('-'): 
        return ['help'] + args
    else:
        return args
