from typing import List

from guet.config.committer import Committer
from guet.context.author_observer import AuthorObserver


class AuthorObservable:
    def __init__(self):
        self.author_observers: List[AuthorObserver] = []

    def add_author_observer(self, observer: AuthorObserver):
        self.author_observers.append(observer)

    def remove_author_observer(self, observer: AuthorObserver):
        self.author_observers.remove(observer)

    def notify_author_observer(self, new_author: Committer):
        for observer in self.author_observers:
            observer.notify_of_author(new_author)
