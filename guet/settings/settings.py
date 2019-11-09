from typing import List

from guet.settings.boolean_parser import boolean_parser
from guet.settings.setting import Setting


class Settings:

    def __init__(self):
        self.version = None
        self._settings = dict()
        self._settings['pairReset'] = Setting(default_value=True,
                                              parser=boolean_parser,
                                              validator=lambda v: type(v) == bool)
        self._settings['debug'] = Setting(default_value=False,
                                          parser=boolean_parser,
                                          validator=lambda v: type(v) == bool)

    def load(self, configuration_file_lines: List[str]):
        lines_without_version = configuration_file_lines[2:]
        self.version = configuration_file_lines[0].rstrip()
        [self._load_attribute(attribute) for attribute in lines_without_version]

    def _load_attribute(self, attribute):
        split = attribute.rstrip().split('=')
        key = split[0]
        value = split[1]
        try:
            self.set(key, value)
        except KeyError:
            print(f'Unknown configuration value \"{key}\" in configuration file.')
            exit(1)

    def write(self) -> List[str]:
        version = [f'{self.version}\n', '\n']
        settings = [self._convert_to_line(key) for key in self._settings if not self._settings[key].is_default_value()]
        return version + settings

    def set(self, key: str, value) -> None:
        read_writer = self._settings[key]
        read_writer.value = read_writer.parser(value)
        self._settings[key] = read_writer

    def read(self, key: str) -> Setting:
        return self._settings[key].value

    def _convert_to_line(self, attribute_key: str) -> str:
        return f'{attribute_key}={self.read(attribute_key)}\n'
