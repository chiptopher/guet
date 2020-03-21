from unittest import TestCase
from unittest.mock import patch

from guet.committers.global_committer import GlobalCommitter


@patch('guet.committers.global_committer.add_committer')
class TestGlobalCommitterSave(TestCase):
    def test_adds_committer_on_save(self, mock_add_committer):
        committer = GlobalCommitter(name='name', email='email', initials='initials')
        committer.save()
        mock_add_committer.assert_called_with('initials', 'name', 'email')
