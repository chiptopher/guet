from guet.commands.command_factory import CommandFactoryMethod


def guet_usage(command_builder_map: dict) -> str:
    help_message = 'usage: guet <command>\n'
    for key in command_builder_map:
        short_help_message = ''
        if not isinstance(command_builder_map[key], CommandFactoryMethod):
            short_help_message = command_builder_map[key].get_short_help_message()
        else:
            short_help_message = command_builder_map[key].short_help_message()
        help_message += f'\n   {key} -- {short_help_message}'
    return help_message + '\n'
