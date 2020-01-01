from unittest import TestCase

from guet.commands.help_message_strategy import HelpMessageBuilder


class TestHelpMessageBuilder(TestCase):

    def test_put_usage_before_usage_description(self):
        builder = HelpMessageBuilder('command args', '')
        self.assertTrue(builder.build().startswith('usage: command args'))

    def test_put_description_after_usage_with_newline_between(self):
        builder = HelpMessageBuilder('command args', 'description')
        result = builder.build()
        self.assertTrue(result.startswith('usage: command args\n\ndescription'))

    def test_end_with_newline_character(self):
        builder = HelpMessageBuilder('command args', 'description')
        result = builder.build()
        self.assertTrue(result.endswith('\n'))

    def test_adding_explanation_puts_it_after_description(self):
        builder = HelpMessageBuilder('command args', 'description').explanation('explanation')
        result = builder.build()
        self.assertTrue('description\n\nexplanation' in result)
