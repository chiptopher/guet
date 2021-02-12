from typing import Dict, List


class DockerFile:
    def __init__(self, path: str):
        self.path = path
        self.lines = []

    def __repr__(self):
        return f'[{self.path}, {self.lines}]'


class FileSystem:
    def __init__(self, files: List[DockerFile]):
        self.files = files

    def get_file(self, path: str) -> DockerFile:
        for file in self.files:
            if file.path == path:
                return file
        return None

    def get_file_from_root(self, path: str) -> DockerFile:
        return self.get_file(f'/root/{path}')

    def get_file_from_test_env(self, path: str) -> DockerFile:
        return self.get_file_from_root(f'test-env/{path}')


def process_file_system(docker_container) -> FileSystem:
    return FileSystem(_convert_file_system_to_include_text(docker_container.diff()))


def _convert_file_system_to_include_text(docker_file_system: List[Dict]) -> List[DockerFile]:
    if docker_file_system is None:
        return []
    return [_convert_docker_file(docker_file) for docker_file in docker_file_system]


def _convert_docker_file(docker_file: Dict) -> DockerFile:
    file_path = docker_file['Path']
    converted_file = DockerFile(file_path)
    return converted_file
