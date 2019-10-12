
from guet.git._create_hook_create_strategy import _HookCreateStrategy


class _PostCommitStrategy(_HookCreateStrategy):
    def name(self) -> str:
        return 'post-commit'

    def file_lines(self) -> [str]:
        return [
            '#! /usr/bin/env python3\n',
            'from guet.commit import PostCommitManager\n',
            'cm = PostCommitManager()\n',
            'cm.manage()\n',
        ]
