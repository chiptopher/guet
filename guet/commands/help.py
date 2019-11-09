from guet.commands.command import Command


class HelpCommand(Command):
    _REQUIRED_ARGS_IN_CORRECT_ORDER = []

    def __init__(self, args, command_builder_map=None):
        super().__init__(args)
        if command_builder_map is None:
            command_builder_map = dict()
        self.command_builder_map = command_builder_map

    def help(self):
        help_message = 'usage: guet <command>\n'
        for key in self.command_builder_map:
            short_help_message = self.command_builder_map[key].get_short_help_message()
            help_message += '\n   {} -- {}'.format(key, short_help_message)
        return help_message + '\n'

    def execute_hook(self) -> None:
        pass

    @classmethod
    def help_short(cls) -> str:
        pass
