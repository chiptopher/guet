from typing import List


class _Builder:

    def build(self) -> str:
        raise NotImplementedError


class _NoneSection(_Builder):

    def build(self) -> str:
        return ''


class _SectionBuild(_Builder):
    def __init__(self, s: str):
        self._str = s

    def build(self) -> str:
        return f'\n{self._str}\n'


class FlagBuilder(_Builder):
    def __init__(self, key: str, value: str):
        self._key = key
        self._value = value

    def build(self) -> str:
        return f'\t{self._key}  -  {self._value}'


class FlagsBuilder(_Builder):
    def __init__(self, flags: List[FlagBuilder]):
        self._flags = flags

    def build(self) -> str:
        flags = "\n".join([f.build() for f in self._flags])
        return f'\nFlags\n{flags}\n'


class HelpMessageBuilder(_Builder):

    def __init__(self, usage: str, description: str):
        self._usage: str = usage
        self._description: _Builder = _SectionBuild(description)
        self._explanation: _Builder = _NoneSection()
        self._flags: _Builder = _NoneSection()

    def explanation(self, explanation: str):
        self._explanation = _SectionBuild(explanation)
        return self

    def flags(self, flags_builder: FlagsBuilder):
        self._flags = flags_builder
        return self

    def build(self) -> str:
        message = (f'usage: {self._usage}\n'
                   f'{self._description.build()}'
                   f'{self._explanation.build()}'
                   f'{self._flags.build()}'
                   f'\n')
        return message
