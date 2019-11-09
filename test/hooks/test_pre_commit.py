import datetime
import unittest
from unittest.mock import patch

from guet.currentmillis import current_millis
from guet.hooks.pre_commit import pre_commit


class TestPreCommit(unittest.TestCase):
    @patch('guet.hooks.pre_commit.most_recent_committers_set')
    @patch('builtins.print')
    @patch('builtins.exit')
    def test_manage_checks_for_most_recent_pair_set_and_exits_1_if_it_is_over_24_hours(self,
                                                                                       mock_exit,
                                                                                       mock_print,
                                                                                       mock_most_recent_committers_set):
        twenty_four_hours = 86400000
        now = current_millis()
        mock_most_recent_committers_set.return_value = now - 100 - twenty_four_hours

        pre_commit()

        mock_exit.assert_called_once_with(1)
        mock_print.assert_called_with(
            "\nYou have not reset pairs in over twenty four hours!\nPlease reset your pairs by using guet set and including your pairs' initials\n")

    @patch('guet.hooks.pre_commit.most_recent_committers_set')
    @patch('builtins.print')
    @patch('builtins.exit')
    def test_manage_checks_for_most_recent_pair_set_and_exits_0_if_it_is_under_24_hours(self,
                                                                                        mock_exit,
                                                                                        mock_print,
                                                                                        mock_most_recent_committers_set):
        ten_hours = 36000000
        now = round((datetime.datetime.utcnow().timestamp() - 1) * 1000)
        mock_most_recent_committers_set.return_value = now - ten_hours
        pre_commit()

        mock_exit.assert_called_once_with(0)
