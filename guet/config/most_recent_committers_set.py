from os.path import join

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.files.read_lines import read_lines
from guet.config.parse_comitters_set_line import parse_committers_set_line


def most_recent_committers_set():
    path = join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET)
    lines = read_lines(path)
    *committer_initials, set_time, path_to_git = parse_committers_set_line(lines[0])
    return int(set_time)
