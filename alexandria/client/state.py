from enum import Enum


class State(Enum):
    TENTATIVE = 0
    CONFIRMED = 1
    DELETED = 2
    DEPRECATED = 3

    def __str__(self):
        return self.name
