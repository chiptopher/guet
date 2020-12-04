from typing import List, Callable

from guet.errors import UnexpectedError

from .step import Step


class OptionStep(Step):

    def __init__(self, choices: List[Step], choice: Callable[[List[str]], int]):
        self.choices = choices
        self.choice = choice

    def do_play(self, args: List[str]):
        desired_choice = self.choice(args)
        if self._has_desired_choice(desired_choice):
            return self.choices[desired_choice]
        else:
            raise UnexpectedError(
                f'Attempting to choose {desired_choice} from {args}')

    def _has_desired_choice(self, position: int) -> bool:
        return (len(self.choices) - 1) >= position
