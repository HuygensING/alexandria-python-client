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

class Annotator:
    """
    Someone who can make text annotations
    """

    def __init__(self, name, description=""):
        """
        :param name:
        :type str:
        :param description:
        :type str:
        """
        self.name = name
        self.description = description

    @property
    def entity(self):
        return {'annotator': {'description': self.description}}

    def __repr__(self):
        return "Annotator::" + self.name + " (" + self.description + ")"
