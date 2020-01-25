from typing import List


def read_lines(path: str) -> List[str]:
    file = open(path, 'r')
    lines = [line.rstrip() for line in file.readlines()]
    file.close()
    return lines
