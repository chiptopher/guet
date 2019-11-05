from typing import List


def read_lines(path: str) -> List[str]:
    f = open(path, 'r')
    lines = f.readlines()
    f.close()
    return lines
