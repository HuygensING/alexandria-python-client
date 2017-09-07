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

from antioch.client.rest_result import RestResult


class RestRequester:
    def __init__(self, response_supplier):
        self.status_mappers = {}
        self.response_supplier = response_supplier

    def on_status(self, status, func):
        self.status_mappers[status] = func
        return self

    def invoke(self):
        response = self.response_supplier()
        try:
            return self.status_mappers[response.status_code](response)
        except KeyError:
            return RestResult(failed=True, response=response)
