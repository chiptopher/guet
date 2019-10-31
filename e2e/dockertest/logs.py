from typing import List

from e2e.dockertest.file_system import FileSystem


def process_logs(docker_container, file_system: FileSystem) -> List[str]:
    return _process_logs(docker_container, file_system)


def _process_logs(container, file_system: FileSystem):
    actual_logs = container.logs()
    encoded = actual_logs.decode('utf-8')
    split = encoded.split('\n')
    logs = _remove_cat_logs(split, file_system)
    return logs


def _remove_cat_logs(current_logs: List[str], file_system: FileSystem):
    line_number_of_start_cat_logs = []
    line_number_of_end_cat_logs = []
    final_logs = current_logs
    for index, line in enumerate(current_logs, start=0):
        if line.startswith('start cat'):
            line_number_of_start_cat_logs.append(index)
        if line.startswith('end cat'):
            line_number_of_end_cat_logs.append(index)
    while len(line_number_of_start_cat_logs) > 0 and len(line_number_of_end_cat_logs) > 0:
        start = line_number_of_start_cat_logs.pop()
        end = line_number_of_end_cat_logs.pop()
        _load_lines_for_file(start, end, final_logs, file_system)
        final_logs = final_logs[:start] + final_logs[end + 1:]
    return final_logs


def _load_lines_for_file(start: int, end: int, final_logs: List[str], file_system: FileSystem):
    file_name = final_logs[start].split('start cat for ')[1]
    file = file_system.get_file(f'/root/{file_name}')
    file.lines = final_logs[0:end][start + 1:]
