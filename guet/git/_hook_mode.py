from enum import Enum


def _append_nothing(base_name: str):
    return base_name


def _append_guet(base_name: str):
    return base_name + '-guet'


def _should_not_be_called(_unused: str):
    return RuntimeError


class HookMode(Enum):
    NEW_OR_OVERWRITE = _append_nothing
    CREATE_ALONGSIDE = _append_guet
    CANCEL = _should_not_be_called
