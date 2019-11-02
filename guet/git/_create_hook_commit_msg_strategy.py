from guet.git._create_hook_create_strategy import _HookCreateStrategy


class _CommitMsgStrategy(_HookCreateStrategy):
    def name(self) -> str:
        return 'commit-msg'

    def file_lines(self) -> [str]:
        return [
            '#! /usr/bin/env python3\n',
            'from guet.hooks import manage\n',
            'import sys\n',
            'manage(sys.argv[0])\n',
        ]
