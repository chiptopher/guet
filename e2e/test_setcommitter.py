

import subprocess
from os.path import join, expanduser

from e2e import DockerTest
from guet import constants as const
from guet.gateways.gateway import PairSetGatewayCommitterGateway


class TestGuetSet(DockerTest):

    def test_set_adds_given_users_to_committers_file(self):
        self.guet_init()

        initials = 'initials'
        name = 'name'
        email = 'user@localhost'

        self.guet_add(initials, name, email)
        self.guet_set([initials])
        self.save_file_content('.guet/committernames')
        self.save_file_content('.guet/authornames')
        self.save_file_content('.guet/authoremails')

        self.execute()

        committer_names = self.get_file_text('.guet/committernames')

        self.assertEqual('{} <{}>'.format(name, email), committer_names[0])
        self.assertEqual(email, self.get_file_text('.guet/authoremails')[0])
        self.assertEqual(name, self.get_file_text('.guet/authornames')[0])


    def test_set_adds_multiple_users_to_committers_file(self):
        self.guet_init()

        initials = 'initials'
        initials2 = 'initials2'
        name = 'name'
        email = 'user@localhost'

        self.guet_add(initials, name, email)
        self.guet_add(initials2, name, email)
        self.guet_set([initials, initials2])
        self.save_file_content('.guet/committernames')

        self.execute()

        committer_names = self.get_file_text('.guet/committernames')

        self.assertEqual('{} <{}>'.format(name, email), committer_names[0])
        self.assertEqual('{} <{}>'.format(name, email), committer_names[1])

    def test_set_gracefully_displays_error_message_when_setting_committer_with_unknown_initials(self):
        self.guet_init()
        self.guet_set(['ui'])

        self.execute()

        self.assert_text_in_logs(0, "No committer exists with initials 'ui'")
