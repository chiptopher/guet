from guet.commands import Command, HelpCommand


class CommandFactory:
    def __init__(self, command_builder_map):
        self.command_builder_map = command_builder_map

    def create(self, args: list) -> Command:
        if len(args) > 0:
            command_arg = args[0]
            initialized_command = self.command_builder_map[command_arg](args)
            return initialized_command
        else:
            return HelpCommand(args, self.command_builder_map)
