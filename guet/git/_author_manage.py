from typing import List

from guet.git.author import Author


def get_author_lines(config_lines: List[str]):
    user = next((line for line in config_lines if line.startswith('\tname = ')), None)
    email = next((line for line in config_lines if line.startswith('\temail = ')), None)
    return user, email


def load_author(config_lines: List[str]) -> Author:
    user, email = get_author_lines(config_lines)
    if user is None or email is None:
        return None
    else:
        return Author(name=user.replace('\tname = ', ''), email=email.replace('\temail = ', ''))


def overwrite_current_author(current_config: List[str], new_author: Author) -> None:
    for i, line in enumerate(current_config):
        if 'name =' in line:
            current_config[i] = f'\tname = {new_author.name}'
        elif 'email =' in line:
            current_config[i] = f'\temail = {new_author.email}'


def append_new_author(new_lines: List[str], new_author: Author):
    new_lines.append('[user]')
    new_lines.append(f'\tname = {new_author.name}')
    new_lines.append(f'\temail = {new_author.email}')
