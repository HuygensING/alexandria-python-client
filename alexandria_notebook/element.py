import json

from enum import Enum


class Element:
    def __init__(self, name, element_mode, attribute_mode='hideAll'):
        self.name = name
        self.element_mode = element_mode
        self.attribute_mode = attribute_mode
        self.when = None
        self._validate()

    def set_element_mode(self, mode):
        self.element_mode = mode

    def set_attribute_mode(self, mode):
        self.attribute_mode = mode

    def set_when(self, when):
        self.when = when

    def _validate(self):
        self._validate_name(self.name)
        self._validate_element_mode(self.element_mode)
        self._validate_attribute_mode(self.attribute_mode)

    def _validate_name(self, name):
        if not isinstance(name, str):
            raise TypeError('parameter \'name\' should be a str')

    def _validate_element_mode(self, mode):
        if not isinstance(mode, str):
            raise TypeError('parameter \'mode\' should be a str')
        if mode not in ['show', 'hide', 'hideTag']:
            raise ValueError('parameter \'mode\' should be \'show\', \'hide\' or \'hideTag\', is \'{0}\''.format(mode))

    def _validate_attribute_mode(self, mode):
        if not isinstance(mode, str):
            raise TypeError('parameter \'mode\' should be a str')
