import os
from os import getcwd
from os.path import join, isfile, isdir


class GitGateway:
    DEFAULT = 'default'
    CREATE_ALONGSIDE = 'create_alongside'
    OVERWRITE = 'overwrite'
    CANCEL = 'candel'

    def __init__(self, parent_dir: str = getcwd()):
        self._parent_dir = parent_dir

    def add_hooks(self, flag, use_python3_as_interpreter: bool = False):
        if not flag is self.CANCEL:
            self._create_commit_hook(flag)
            self._create_author_manager_script(flag, use_python3_as_interpreter)
            self._create_pre_commit_hook(flag, use_python3_as_interpreter)

    def _create_commit_hook(self, flag):
        lines = [
            "#!/bin/sh",
            "FILE_LOCATION=~/.guet/committernames",
            'CO_AUTHOR="Co-authored-by:"',
            'echo "\\n\\n" >> "$1"',
            'while read committer; do',
            '	echo "$CO_AUTHOR $committer" >> "$1"',
            'done <$FILE_LOCATION'
        ]
        hook_path = join(self._parent_dir, '.git', 'hooks', self._format_file_name_from_flag('commit-msg', flag))
        f = open(hook_path, "w")
        st = os.stat(hook_path)
        os.chmod(hook_path, st.st_mode | 0o111)
        for line in lines:
            f.write(line + '\n')
        f.close()

    def _create_pre_commit_hook(self, flag, use_python3_as_interpreter: bool = False):
        shebang = '#! /usr/bin/env python'
        if use_python3_as_interpreter:
            shebang = shebang + '3'
        lines = [
            shebang,
            'from guet.commit import PreCommitManager',
            'cm = PreCommitManager()',
            'cm.manage()',
        ]
        hook_path = join(self._parent_dir, '.git', 'hooks', self._format_file_name_from_flag('pre-commit', flag))
        f = open(hook_path, 'w')
        st = os.stat(hook_path)
        os.chmod(hook_path, st.st_mode | 0o111)
        for line in lines:
            f.write(line + '\n')
        f.close()

    def commit_msg_hook_exists(self):
        return isfile(join(self._parent_dir, '.git', 'hooks', 'commit-msg'))

    def git_present(self):
        return isdir(join(os.getcwd(), '.git'))

    def _create_author_manager_script(self, flag, use_python3_as_interpreter: bool = False):
        shebang = '#! /usr/bin/env python'
        if use_python3_as_interpreter:
            shebang = shebang + '3'
        lines = [
            shebang,
            'from guet.commit import PostCommitManager',
            'cm = PostCommitManager()',
            'cm.manage()',
        ]
        hook_path = join(self._parent_dir, '.git', 'hooks', self._format_file_name_from_flag('post-commit', flag))
        f = open(hook_path, "w")
        st = os.stat(hook_path)
        os.chmod(hook_path, st.st_mode | 0o111)
        for line in lines:
            f.write(line + '\n')
        f.close()

    def any_hook_present(self):
        return self.hook_present('pre-commit') or self.hook_present('post-commit') or self.hook_present('commit-msg')

    def hook_present(self, file_name: str):
        return isfile(join(self._parent_dir, '.git', 'hooks', file_name))

    def _format_file_name_from_flag(self, default_name, flag):
        if flag == self.CREATE_ALONGSIDE:
            return 'guet-{}'.format(default_name)
        return default_name
