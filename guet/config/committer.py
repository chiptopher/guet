from typing import List


class Committer:
    def __init__(self, name: str, email: str, initials: str):
        self.name = name
        self.email = email
        self.initials = initials

    def __eq__(self, o):
        return self.name == o.name and self.email == o.email and self.initials == o.initials

    def __str__(self):
        return f'{self.initials},{self.name},{self.email}'

    def pretty(self):
        return f'{self.initials} - {self.name} <{self.email}>'

    def save(self):
        raise NotImplementedError()


def filter_committers_with_initials(committers: List[Committer],
                                    initials: List[str]) -> List[Committer]:
    return [committer for committer in committers if committer.initials in initials]
