
from test.commands.test_command import CommandTest, create_test_case
from guet.commands.setcommitters import SetCommittersCommand
from guet.gateway import *
from unittest.mock import Mock


class TestSetCommittersCommand(CommandTest):

    def test_validate(self):
        cases = [
            create_test_case(['set', 'extra'], True, 'Should return true when the correct number of args'),
            create_test_case([], False, 'Should return false when not enough arguments are given'),
            create_test_case(['something else'], False, 'Should return false when the required args are wrong')
        ]

        for case in cases:
            self._validate_test(case, SetCommittersCommand)

    def test_execute_adds_the_people_with_the_initials_to_the_committers_file(self):
        mock_file_gateway = FileGateway()
        mock_file_gateway.set_committers = Mock()

        initials = 'initials'
        name = 'name'
        email = 'email'

        def _mock_user_return(initials: str, ):
            if initials is initials:
                return committer_result(name=name, email=email, initials=initials)

        mock_user_gateway = UserGateway()
        mock_user_gateway.get_user = Mock(side_effect=_mock_user_return)

        command = SetCommittersCommand(['set', initials], mock_user_gateway, mock_file_gateway)
        command.execute()

        mock_file_gateway.set_committers.assert_called_once_with([CommitterInput(email=email, name=name)])
