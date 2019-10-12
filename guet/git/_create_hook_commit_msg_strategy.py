from guet.git._create_hook_create_strategy import _HookCreateStrategy


class _CommitMsgStrategy(_HookCreateStrategy):
    def name(self) -> str:
        return 'commit-msg'

    def file_lines(self) -> [str]:
        return [
            "#!/bin/sh\n",
            "FILE_LOCATION=~/.guet/committernames\n",
            'CO_AUTHOR="Co-authored-by:"\n',
            'echo "\\n\\n" >> "$1"\n',
            'while read committer; do\n',
            '	echo "$CO_AUTHOR $committer" >> "$1"\n',
            'done <$FILE_LOCATION\n'
        ]
