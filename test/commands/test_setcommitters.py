from unittest.mock import Mock, patch

from guet.commands.setcommitters import SetCommittersCommand
from guet.config.committer import Committer
from guet.gateways.gateway import *
from guet.gateways.io import PrintGateway
from test.commands.test_command import CommandTest, create_test_case


@patch('guet.commands.setcommitters.set_committer_as_author')
@patch('guet.commands.setcommitters.set_committers')
class TestSetCommittersCommand(CommandTest):

    def setUp(self):
        self.mock_user_gateway = UserGateway()
        self.mock_user_gateway.get_user = Mock()

        self.mock_pair_set_gateway = PairSetGateway()
        self.mock_pair_set_gateway.add_pair_set = Mock()
        self.mock_pair_set_gateway.get_pair_set = Mock()
        self.mock_pair_set_gateway.get_most_recent_pair_set = Mock()

        self.mock_pair_set_committer_gateway = PairSetGatewayCommitterGateway()
        self.mock_pair_set_committer_gateway.add_pair_set_committer = Mock()
        self.mock_pair_set_committer_gateway.get_pair_set_committers_by_pair_set_id = Mock()

        self.mock_print_gateway = PrintGateway()
        self.mock_print_gateway.print = Mock()

    def test_validate(self,
                      mock_set_committers,
                      mock_set_committer_as_author):
        cases = [
            create_test_case(['set', 'extra'], True, 'Should return true when the correct number of args'),
            create_test_case([], False, 'Should return false when not enough arguments are given'),
            create_test_case(['something else'], False, 'Should return false when the required args are wrong')
        ]

        for case in cases:
            self._validate_test(case, SetCommittersCommand)

    def test_execute_adds_the_people_with_the_initials_to_the_committers_file(self,
                                                                              mock_set_committers,
                                                                              mock_set_committer_as_author):
        initials = 'initials'
        name = 'name'
        email = 'email'

        def _mock_user_return(initials: str, ):
            if initials is initials:
                return committer_result(name=name, email=email, initials=initials)

        self.mock_user_gateway.get_user = Mock(side_effect=_mock_user_return)

        command = self._create_set_committers_command_with_all_mocks(['set', initials], self.mock_user_gateway)
        command.execute()

        mock_set_committers.assert_called_with([Committer(name, email)])

    def test_execute_adds_the_fist_person_in_the_list_as_the_author_email_and_name(self,
                                                                                   mock_set_committers,
                                                                                   mock_set_committer_as_author):
        expected_initials = 'initials'

        def _mock_user_return(initials: str):
            if initials is expected_initials:
                return committer_result(name='name', email='email', initials=expected_initials)

        self.mock_user_gateway.get_user = Mock(side_effect=_mock_user_return)

        command = self._create_set_committers_command_with_all_mocks(['set', expected_initials], self.mock_user_gateway)
        command.execute()
        mock_set_committer_as_author.assert_called_with(Committer('name', 'email'))

    def test_execute_will_add_a_pair_set_and_committers_to_it(self,
                                                              mock_set_committers,
                                                              mock_set_committer_as_author):
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
        self.assertAlmostEqual(round(datetime.datetime.utcnow().timestamp() * 1000), call[0][0], -2)
        self.mock_pair_set_committer_gateway.add_pair_set_committer.assert_called_once_with('initials', pair_set_id)

    def test_execute_prints_out_error_message_when_the_given_initials_arent_in_the_system(self,
                                                                                          mock_set_committers,
                                                                                          mock_set_committer_as_author):
        self.mock_user_gateway.get_user = Mock(return_value=None)
        command = self._create_set_committers_command_with_all_mocks(['set', 'initials'])
        command.execute()
        self.mock_print_gateway.print.assert_called_once_with("No committer exists with initials 'initials'")

    def test_execute_failing_doesnt_set_committers_still(self,
                                                         mock_set_committers,
                                                         mock_set_committer_as_author):
        expected_initials = 'initials'
        name = 'name'
        email = 'email'

        def _mock_user_return(initials: str, ):
            if initials is expected_initials:
                return committer_result(name=name, email=email, initials=initials)

        self.mock_user_gateway.get_user = Mock(side_effect=_mock_user_return)

        command = self._create_set_committers_command_with_all_mocks(['set', expected_initials, 'initials2'])
        command.execute()
        mock_set_committers.assert_not_called()

    def test_execute_should_add_all_pair_set_committers_only_when_all_of_the_committers_exist(self,
                                                                                              mock_set_committers,
                                                                                              mock_set_committer_as_author):
        user1 = committer_result(name='name1', email='email1', initials='initials1')
        user2 = committer_result(name='name2', email='email2', initials='initials2')
        users = {
            'initials1': user1,
            'initials2': user2
        }

        def _mock_user_return(initials: str):
            try:
                return users[initials]
            except KeyError:
                return None

        self.mock_user_gateway.get_user = Mock(side_effect=_mock_user_return)

        command = self._create_set_committers_command_with_all_mocks(['set', 'initials1', 'initials2', 'initials3'])
        command.execute()

        self.mock_pair_set_committer_gateway.add_pair_set_committer.assert_not_called()

    def _create_set_committers_command_with_all_mocks(self,
                                                      args: list,
                                                      mock_user_gateway: UserGateway = None,
                                                      mock_pair_set_gateway: PairSetGateway = None,
                                                      mock_pair_set_committers_gateway: PairSetGatewayCommitterGateway = None,
                                                      mock_print_gateway: PrintGateway = None):
        ug = mock_user_gateway if None else self.mock_user_gateway
        psg = mock_pair_set_gateway if None else self.mock_pair_set_gateway
        pscg = mock_pair_set_committers_gateway if None else self.mock_pair_set_committer_gateway
        pg = mock_print_gateway if None else self.mock_print_gateway
        return SetCommittersCommand(args, ug, psg, pscg, pg)
