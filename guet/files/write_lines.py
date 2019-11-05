from typing import List


def write_lines(path: str, lines: List[str]) -> None:
    f = open(path, 'w')
    f.writelines(lines)
    f.close()
