"""
   Copyright 2017 Huygens ING

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

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
        _validate_name(self.name)
        _validate_element_mode(self.element_mode)
        _validate_attribute_mode(self.attribute_mode)


def _validate_name(name):
    if not isinstance(name, str):
        raise TypeError('parameter \'name\' should be a str')


def _validate_element_mode(mode):
    if not isinstance(mode, str):
        raise TypeError('parameter \'mode\' should be a str')
    if mode not in ['show', 'hide', 'hideTag']:
        raise ValueError('parameter \'mode\' should be \'show\', \'hide\' or \'hideTag\', is \'{0}\''.format(mode))


def _validate_attribute_mode(mode):
    if not isinstance(mode, str):
        raise TypeError('parameter \'mode\' should be a str')
