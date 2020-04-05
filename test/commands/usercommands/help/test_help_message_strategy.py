from unittest import TestCase

from guet.commands.usercommands.help.help_message_builder import HelpMessageBuilder, FlagsBuilder, FlagBuilder


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

    def test_adding_flags_section_adds_flags(self):
        result = HelpMessageBuilder('command args', 'description').flags(
            FlagsBuilder([FlagBuilder('key1', 'value1'), FlagBuilder('key2', 'value2')])).build()
        self.assertTrue('\nFlags\n\tkey1  -  value1\n\tkey2  -  value2\n' in result)
