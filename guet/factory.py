from guet.commands import Command


class CommandFactory:
    def __init__(self, command_builder_map):
        self.command_builder_map = command_builder_map

    def create(self, args: list) -> Command:
        command_arg = args[0]
        initialized_command = self.command_builder_map[command_arg](args)
        return initialized_command
