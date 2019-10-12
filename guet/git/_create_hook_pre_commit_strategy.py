from guet.git._create_hook_create_strategy import _HookCreateStrategy


class _PreCommitStrategy(_HookCreateStrategy):
    def name(self) -> str:
        return 'pre-commit'

    def file_lines(self) -> [str]:
        return [
            '#! /usr/bin/env python3\n',
            'from guet.commit import PreCommitManager\n',
            'cm = PreCommitManager()\n',
            'cm.manage()\n'
        ]
