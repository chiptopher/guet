from typing import List

from guet.git._guet_hooks import GUET_HOOKS
from guet.git.hook import Hook


def _name(hook: Hook) -> str:
    return hook.path.split('/')[-1]


def _normal_hooks(hooks: List[Hook]) -> List[Hook]:
    return [hook for hook in hooks if _name(hook) in GUET_HOOKS]


def _dash_guet_normal_hooks(hooks: List[Hook]) -> List[Hook]:
    final = []
    for hook in hooks:
        name = _name(hook)
        if name.endswith('-guet') and name.replace('-guet', '') in GUET_HOOKS:
            final.append(hook)
    return final


def all_valid_hooks(hooks: List[Hook]) -> bool:
    hook_names = [_name(hook) for hook in _normal_hooks(hooks)]
    valid_names = GUET_HOOKS == hook_names
    valid_content = all([hook.is_guet_hook() for hook in _normal_hooks(hooks)])
    if not (valid_names and valid_content):
        hook_names = [_name(hook).replace('-guet', '') for hook in _dash_guet_normal_hooks(hooks)]
        valid_names = GUET_HOOKS == hook_names
        valid_content = all([hook.is_guet_hook() for hook in _dash_guet_normal_hooks(hooks)])
        return valid_names and valid_content
    return True
