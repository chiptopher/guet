import unittest
from os.path import join
from pathlib import Path
from unittest.mock import patch, Mock, ANY

from guet.config import CONFIGURATION_DIRECTORY

from guet import constants
from guet.committers._add_committer import add_committer


@patch('guet.committers._add_committer.write_lines')
@patch('guet.committers._add_committer.read_lines')
class AddCommitterTest(unittest.TestCase):

    def test_reads_all_contents_from_committers_file_and_overwrites_it_with_committer_added(self, mock_read_lines,
                                                                                            mock_write_lines):
        mock_read_lines.return_value = [
            'initials1,name1,email1\n',
            'initials2,name2,email2\n'
        ]
        add_committer('initials3', 'name3', 'email3')
        mock_write_lines.assert_called_with(Path(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS)), [
            'initials1,name1,email1\n',
            'initials2,name2,email2\n',
            'initials3,name3,email3\n',
        ])

    def test_replaces_committer_if_initials_are_alread_in_committers_file(self, mock_read_lines,
                                                                          mock_write_lines):
        mock_read_lines.return_value = [
            'initials1,name1,email1\n',
            'initials2,name2,email2\n',
            'initials3,name3,email3\n'
        ]
        add_committer('initials2', 'new name2', 'new email2')
        mock_write_lines.assert_called_with(Path(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS)), [
            'initials1,name1,email1\n',
            'initials2,new name2,new email2\n',
            'initials3,name3,email3\n'
        ])

    def test_providing_a_file_path_uses_that_file_path_instead(self, mock_read_lines, mock_write_lines):
        path: Path = Mock()
        add_committer('initials3', 'name3', 'email3', file_path=path)
        mock_read_lines.assert_called_with(path)
        mock_write_lines.assert_called_with(path, ANY)

    def test_writes_to_file_with_committer_if_file_not_found(self, mock_read_lines, mock_write_lines):
        mock_read_lines.side_effect = FileNotFoundError()
        add_committer('initials', 'name', 'email')
        mock_write_lines.assert_called_with(Path(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS)), [
            'initials,name,email\n',
        ])
