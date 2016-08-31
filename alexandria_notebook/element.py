import json

from enum import Enum


class ElementMode(Enum):
    show = 0
    hide = 1
    hideTag = 2


class Element:
    def __init__(self, name):
        self.name = name
        self.element_mode = ''
        self.attribute_mode = ''

    def set_element_mode(self, mode):
        self.element_mode = mode
        return self

    def set_attribute_mode(self, mode):
        self.attribute_mode = mode
        return self

    def __repr__(self):
        return json.dumps(self.__dict__)
