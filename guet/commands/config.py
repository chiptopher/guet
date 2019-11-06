from guet.commands import Command


class ConfigSetCommand(Command):
    HELP_MESSAGE = 'usage: guet config [--<key>=<value> ...]'
    SHORT_HELP_MESSAGE = 'Change setting values'

    def execute(self):
        pass

    def help(self) -> str:
        return self.HELP_MESSAGE

    @classmethod
    def get_short_help_message(cls):
        return cls.SHORT_HELP_MESSAGE
