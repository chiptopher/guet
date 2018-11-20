from test.commands.test_command import CommandTest, create_test_case
from guet.commands.setcommitters import SetCommittersCommand
from guet.gateway import *
from unittest.mock import Mock


class TestSetCommittersCommand(CommandTest):

    def setUp(self):
        self.mock_file_gateway = FileGateway()
        self.mock_file_gateway.set_committers = Mock()
        self.mock_file_gateway.set_author_email = Mock()
        self.mock_file_gateway.set_author_name = Mock()

        self.mock_user_gateway = UserGateway()
        self.mock_user_gateway.get_user = Mock()

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
        # def _mock_user_return(initials: str):
            # return committer_result(name='name', email=)

    def _create_set_committers_command_with_all_mocks(self,
                                                      args,
                                                      mock_user_gateway: UserGateway = Mock(),
                                                      mock_file_gateway: FileGateway = Mock(),
                                                      mock_pair_set_gateway: PairSetGateway = Mock(),
                                                      mock_pair_set_committers_gateway: PairSetGatewayCommitterGateway = Mock()):
        return SetCommittersCommand(args, mock_user_gateway, mock_file_gateway, mock_pair_set_gateway,
                                    mock_pair_set_committers_gateway)
