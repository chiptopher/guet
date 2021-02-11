from unittest import TestCase
from unittest.mock import Mock, patch

from guet.committers._initials_for_project import initials_for_project

from guet.committers._committers_set import CommittersSet


@patch('guet.committers._initials_for_project.all_committers_set')
@patch('guet.committers._initials_for_project.current_millis')
class TestInitialsForPorject(TestCase):
    def test_returns_initials_for_project_with_given_path(self, mock_millis, mock_all_committers_set):
        found = CommittersSet(['initials1', 'initials2'],
                              100, 'path/to/project/root')

        mock_all_committers_set.return_value = [found]
        mock_millis.return_value = 100

        result = initials_for_project('path/to/project/root')
        self.assertEqual(['initials1', 'initials2'], result)
