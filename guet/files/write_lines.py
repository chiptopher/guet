from typing import List


def _append_newline_if_not_present(line: str):
    if line.endswith('\n'):
        return line
    else:
        return f'{line}\n'


def write_lines(path: str, lines: List[str]) -> None:
    file = open(path, 'w')
    file.writelines([_append_newline_if_not_present(line) for line in lines])
    file.close()
