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

# from alexandria_notebook.element import Element


class TextView:
    def __init__(self, name):
        self.name = name
        self.description = ""
        self.elements = []

    def __dir__(self):
        return ['name', 'description', 'elements']

    @property
    def entity(self):
        element_dict = {}
        for e in self.elements:
            element_dict[e.name] = {'elementMode': e.element_mode, 'attributeMode': e.attribute_mode}
            if e.when is not None:
                element_dict[e.name]['when'] = e.when
        return {'textView': {'description': self.description, 'elements': element_dict}}
