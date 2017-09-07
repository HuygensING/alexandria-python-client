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

class TextAnnotation:
    def __init__(self, name, annotator_id, position, attributes=None):
        self.name = name
        self.annotator = annotator_id
        self.position = position
        self.attributes = attributes

    @property
    def entity(self):
        position = {'xml:id': self.position.xml_id}
        if self.position.offset is not None:
            position['offset'] = self.position.offset
            position['length'] = self.position.length
        annotation = {'name': self.name, 'annotator': self.annotator,
                      'position': position}
        if self.attributes is not None:
            annotation['attributes'] = self.attributes
        entity = {
            'textAnnotation': annotation}
        return entity
