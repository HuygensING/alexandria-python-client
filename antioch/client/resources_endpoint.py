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

import time
from http import HTTPStatus

import antioch.client.util as util
from antioch.client.antioch_endpoint import AntiochEndpoint
from antioch.client.annotator import Annotator
from antioch.client.rest_requester import RestRequester
from antioch.client.state import *
from antioch.client.state_prototype import *


class ResourcesEndpoint(AntiochEndpoint):
    endpoint = 'resources'
    state = 'state'

    def add(self, proto):
        def adder():
            return self.antioch.post(self.endpoint, proto.entity)

        add_result = RestRequester(adder).on_status(HTTPStatus.CREATED, util.location_as_uuid).invoke()

        if self.antioch.auto_confirm and not add_result.failed:
            self.confirm(add_result.uuid)

        return add_result

    def confirm(self, uuid):
        def confirm():
            uri = self.resource_state_uri(uuid)
            data = StatePrototype(State.CONFIRMED).entity
            return self.antioch.put(uri=uri, data=data)

        return RestRequester(confirm).on_status(HTTPStatus.NO_CONTENT, util.response_as_is).invoke()

    def get(self, uuid):
        def getter():
            return self.antioch.get(util.endpoint_uri(self.endpoint, uuid))

        return RestRequester(getter).on_status(HTTPStatus.OK, util.entity_as_json).invoke()

    def set(self, uuid, proto):
        def updater():
            return self.antioch.put(uri=util.endpoint_uri(self.endpoint, uuid), data=proto.entity)

        return RestRequester(updater) \
            .on_status(HTTPStatus.OK, util.entity_as_json) \
            .on_status(HTTPStatus.CREATED, util.location_as_uuid) \
            .on_status(HTTPStatus.NO_CONTENT, util.response_as_is) \
            .invoke()

    def resource_uri(self, uuid):
        return util.endpoint_uri(self.endpoint, uuid)

    def resource_state_uri(self, uuid):
        return util.endpoint_uri(self.endpoint, uuid, self.state)

    def set_text(self, uuid, xml):
        def setter():
            return self.antioch.put_data(uri=util.endpoint_uri(self.endpoint, uuid, 'text'), data=xml)

        def status_getter():
            return self.antioch.get(uri=util.endpoint_uri(self.endpoint, uuid, 'text', 'status'))

        RestRequester(setter) \
            .on_status(HTTPStatus.OK, util.response_as_is) \
            .invoke()
        done = False
        while not done:
            time.sleep(1)
            status = RestRequester(status_getter) \
                .on_status(HTTPStatus.OK, util.entity_as_json) \
                .invoke().json
            done = status['textImportStatus']['done']
        return status

    def get_text(self, uuid):
        def getter():
            return self.antioch.get(util.endpoint_uri(self.endpoint, uuid, 'text', 'xml'))

        return RestRequester(getter).on_status(HTTPStatus.OK, util.response_as_is).invoke().response.text

    def get_text_using_view(self, uuid, view_name):
        def getter():
            return self.antioch.get(
                util.endpoint_uri(self.endpoint, uuid, 'text', 'xml') + "?view=" + view_name)

        return RestRequester(getter).on_status(HTTPStatus.OK, util.response_as_is).invoke().response.text

    def get_dot(self, uuid):
        def getter():
            return self.antioch.get(util.endpoint_uri(self.endpoint, uuid, 'text', 'dot'))

        return RestRequester(getter).on_status(HTTPStatus.OK, util.response_as_is).invoke().response.text

    def set_view(self, uuid, name, view):
        def updater():
            return self.antioch.put(uri=util.endpoint_uri(self.endpoint, uuid, 'text', 'views', name),
                                    data=view.entity)

        return RestRequester(updater).on_status(HTTPStatus.OK, util.response_as_is).invoke().response.text

    def set_annotator(self, uuid, annotator):
        def updater():
            return self.antioch.put(uri=util.endpoint_uri(self.endpoint, uuid, 'annotators', annotator.name),
                                    data=annotator.entity)

        return RestRequester(updater).on_status(HTTPStatus.OK, util.response_as_is).invoke().response.text

    def get_annotators(self, uuid):
        def getter():
            return self.antioch.get(util.endpoint_uri(self.endpoint, uuid, 'annotators'))

        json = RestRequester(getter).on_status(HTTPStatus.OK, util.response_as_is).invoke().response.json()
        annotators = [Annotator(a['annotator']['code'], a['annotator']['description']) for a in json]
        return annotators

    def set_text_annotation(self, uuid, text_annotation):
        def updater():
            import uuid as uuid_mod
            annotation_uuid = uuid_mod.uuid1()
            return self.antioch.put(
                uri=util.endpoint_uri(self.endpoint, uuid, 'text', 'annotations', annotation_uuid),
                data=text_annotation.entity)

        return RestRequester(updater).on_status(HTTPStatus.OK, util.response_as_is).invoke().response.text

    def add_unique_ids(self, uuid, elements):
        resource_ids = [uuid]
        cargo = {"resourceIds": resource_ids, "elements": elements}

        def poster():
            return self.antioch.post(uri=util.endpoint_uri('commands', 'add-unique-id'), data=cargo)

        return RestRequester(poster).on_status(HTTPStatus.OK, util.response_as_is).invoke().response.text
