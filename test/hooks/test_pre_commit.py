import datetime
import unittest
from unittest.mock import patch

from guet.currentmillis import current_millis
from guet.hooks.pre_commit import pre_commit
from guet.settings.settings import Settings


@patch('guet.hooks.pre_commit.get_config', return_value=Settings())
@patch('guet.hooks.pre_commit.most_recent_committers_set')
@patch('builtins.print')
@patch('builtins.exit')
class TestPreCommit(unittest.TestCase):
    def test_manage_checks_for_most_recent_pair_set_and_exits_1_if_it_is_over_24_hours(
            self, mock_exit, mock_print, mock_most_recent_committers_set, mock_get_config):
        twenty_four_hours = 86400000
        now = current_millis()
        mock_most_recent_committers_set.return_value = now - 100 - twenty_four_hours

        pre_commit()

        mock_exit.assert_called_once_with(1)
        mock_print.assert_called_with(
            "\nYou have not reset pairs in over twenty four hours!\nPlease reset your pairs by using guet set and including your pairs' initials\n"
        )

    def test_manage_checks_for_most_recent_pair_set_and_exits_0_if_it_is_under_24_hours(
            self, mock_exit, mock_print, mock_most_recent_committers_set, mock_get_config):
        ten_hours = 36000000
        now = round((datetime.datetime.utcnow().timestamp() - 1) * 1000)
        mock_most_recent_committers_set.return_value = now - ten_hours
        pre_commit()

        mock_exit.assert_not_called()

    def test_wont_error_when_time_is_over_24_hours_if_pair_reset_is_disabled(
            self, mock_exit, mock_print, mock_most_recent_committers_set, mock_get_config):
        twenty_four_hours = 86400000
        now = current_millis()
        mock_most_recent_committers_set.return_value = now - 100 - twenty_four_hours
        pair_reset_disabled_settings = Settings()
        pair_reset_disabled_settings.set('pairReset', 'False')
        mock_get_config.return_value = pair_reset_disabled_settings

        pre_commit()

        mock_exit.assert_not_called()