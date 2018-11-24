import datetime
from unittest.mock import Mock

from guet.commands.setcommitters import SetCommittersCommand
from guet.gateway import *
from test.commands.test_command import CommandTest, create_test_case


class TestSetCommittersCommand(CommandTest):

    def setUp(self):
        self.mock_file_gateway = FileGateway()
        self.mock_file_gateway.set_committers = Mock()
        self.mock_file_gateway.set_author_email = Mock()
        self.mock_file_gateway.set_author_name = Mock()

        self.mock_user_gateway = UserGateway()
        self.mock_user_gateway.get_user = Mock()

        self.mock_pair_set_gateway = PairSetGateway()
        self.mock_pair_set_gateway.add_pair_set = Mock()
        self.mock_pair_set_gateway.get_pair_set = Mock()
        self.mock_pair_set_gateway.get_most_recent_pair_set = Mock()

        self.mock_pair_set_committer_gateway = PairSetGatewayCommitterGateway()
        self.mock_pair_set_committer_gateway.add_pair_set_committer = Mock()
        self.mock_pair_set_committer_gateway.get_pair_set_committers_by_pair_set_id = Mock()

    def test_validate(self):
        cases = [
            create_test_case(['set', 'extra'], True, 'Should return true when the correct number of args'),
            create_test_case([], False, 'Should return false when not enough arguments are given'),
            create_test_case(['something else'], False, 'Should return false when the required args are wrong')
        ]

        for case in cases:
            self._validate_test(case, SetCommittersCommand)

    def test_execute_adds_the_people_with_the_initials_to_the_committers_file(self):
        initials = 'initials'
        name = 'name'
        email = 'email'

        def _mock_user_return(initials: str, ):
            if initials is initials:
                return committer_result(name=name, email=email, initials=initials)

        self.mock_user_gateway.get_user = Mock(side_effect=_mock_user_return)

        command = self._create_set_committers_command_with_all_mocks(['set', initials], self.mock_user_gateway,
                                                                     self.mock_file_gateway)
        command.execute()

        self.mock_file_gateway.set_committers.assert_called_once_with([CommitterInput(email=email, name=name)])

    def test_execute_adds_the_fist_person_in_the_list_as_the_author_email_and_name(self):
        expected_initials = 'initials'

        def _mock_user_return(initials: str):
            if initials is expected_initials:
                return committer_result(name='name', email='email', initials=expected_initials)

        self.mock_user_gateway.get_user = Mock(side_effect=_mock_user_return)

        command = self._create_set_committers_command_with_all_mocks(['set', expected_initials], self.mock_user_gateway,
                                                                     self.mock_file_gateway)
        command.execute()
        self.mock_file_gateway.set_author_email.assert_called_once_with('email')
        self.mock_file_gateway.set_author_name.assert_called_once_with('name')

    def test_execute_will_add_a_pair_set_and_committers_to_it(self):
        pair_set_id = 2
        def _mock_user_return(initials: str):
            return committer_result(name='name', email='email', initials='initials')

        self.mock_user_gateway.get_user = Mock(side_effect=_mock_user_return)

        def _mock_add_pair(pair_set_time: int):
            return pair_set_id

        self.mock_pair_set_gateway.add_pair_set = Mock(side_effect=_mock_add_pair)
        command = self._create_set_committers_command_with_all_mocks(['set', 'initials'], self.mock_user_gateway)
        command.execute()

        call = self.mock_pair_set_gateway.add_pair_set.call_args_list[0]
        self.assertAlmostEqual(round(datetime.datetime.utcnow().timestamp()*1000), call[0][0], -2)
        self.mock_pair_set_committer_gateway.add_pair_set_committer.assert_called_once_with('initials', pair_set_id)

    def _create_set_committers_command_with_all_mocks(self,
                                                      args: list,
                                                      mock_user_gateway: UserGateway = None,
                                                      mock_file_gateway: FileGateway = None,
                                                      mock_pair_set_gateway: PairSetGateway = None,
                                                      mock_pair_set_committers_gateway: PairSetGatewayCommitterGateway = None):
        ug = mock_user_gateway if None else self.mock_user_gateway
        fg = mock_file_gateway if None else self.mock_file_gateway
        psg = mock_pair_set_gateway if None else self.mock_pair_set_gateway
        pscg = mock_pair_set_committers_gateway if None else self.mock_pair_set_committer_gateway
        return SetCommittersCommand(args, ug, fg, psg, pscg)
