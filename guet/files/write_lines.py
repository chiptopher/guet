from typing import List


def write_lines(path: str, lines: List[str]) -> None:
    file = open(path, 'w')
    file.writelines(lines)
    file.close()
