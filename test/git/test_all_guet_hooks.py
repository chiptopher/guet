from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, call, patch

from guet.git._all_guet_hooks import all_guet_hooks


@patch('guet.git._all_guet_hooks.project_root', return_value=Path('project/root'))
class TestAllGuetHooks(TestCase):

    def test_loads_all_expected_hooks(self, mock_project_root):
        mock_file = Mock()
        mock_file.read.return_value = []

        file_system = Mock()
        file_system.get.return_value = mock_file

        all_guet_hooks(file_system)

        hooks_path = mock_project_root.return_value.joinpath('.git').joinpath('hooks')

        file_system.get.assert_has_calls([
            call(hooks_path.joinpath('pre-commit')),
            call().read(),
            call(hooks_path.joinpath('post-commit')),
            call().read(),
            call(hooks_path.joinpath('commit-msg')),
            call().read(),
            call(hooks_path.joinpath('pre-commit-guet')),
            call().read(),
            call(hooks_path.joinpath('post-commit-guet')),
            call().read(),
            call(hooks_path.joinpath('commit-msg-guet')),
            call().read(),
        ])

    def test_only_returns_files_with_guet_content(self, _1):
        mock_with = Mock()
        mock_with.read.return_value = [
            '#! /usr/bin/env python3',
            'from guet.hooks import run',
            'import sys',
            'run(sys.argv[0])',
        ]
        mock_without = Mock()
        mock_without.read.return_value = [
            'some',
            'other',
            'lines',
        ]

        file_system = Mock()
        file_system.get.side_effect = [
            mock_with,
            mock_without,
            mock_with,
            mock_without,
            mock_with,
            mock_without,
        ]

        result = all_guet_hooks(file_system)

        self.assertEqual([mock_with, mock_with, mock_with], result)
