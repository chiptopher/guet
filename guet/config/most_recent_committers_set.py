from os.path import join

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.errors import PairSetError
from guet.files.read_lines import read_lines
from guet.config.parse_comitters_set_line import parse_committers_set_line
from guet.git.git_path_from_cwd import git_path_from_cwd


def most_recent_committers_set():
    path = join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET)
    lines = read_lines(path)
    try:
        line = next(line for line in lines if line.endswith(git_path_from_cwd()))
        *_, set_time, _ = parse_committers_set_line(line)
        return int(set_time)
    except StopIteration:
        raise PairSetError()
