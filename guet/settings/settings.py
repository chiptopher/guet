from typing import List

from guet.settings.boolean_parser import boolean_parser
from guet.settings.setting import Setting


class Settings:

    def __init__(self):
        self.version = None
        self._settings = dict()
        self._settings['pairReset'] = Setting(default_value=True,
                                              parser=boolean_parser,
                                              validator=lambda v: isinstance(v, bool))
        self._settings['debug'] = Setting(default_value=False,
                                          parser=boolean_parser,
                                          validator=lambda v: isinstance(v, bool))

    def load(self, configuration_file_lines: List[str]):
        lines_without_version = configuration_file_lines[2:]
        self.version = configuration_file_lines[0].rstrip()
        for attribute in lines_without_version:
            self._load_attribute(attribute)

    def _load_attribute(self, attribute):
        key, value = attribute.rstrip().split('=')
        try:
            self.set(key, value)
        except KeyError:
            print(f'Unknown configuration value \"{key}\" in configuration file.')
            exit(1)

    def write(self) -> List[str]:
        version = [f'{self.version}\n', '\n']
        settings = []
        for key in self._settings:
            if not self._settings[key].is_default_value():
                settings.append(self._convert_to_line(key))
        return version + settings

    def set(self, key: str, value) -> None:
        read_writer = self._settings[key]
        read_writer.value = read_writer.parser(value)
        self._settings[key] = read_writer

    def read(self, key: str) -> Setting:
        return self._settings[key].value

    def _convert_to_line(self, attribute_key: str) -> str:
        return f'{attribute_key}={self.read(attribute_key)}\n'
