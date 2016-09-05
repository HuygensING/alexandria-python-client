import time
from http import HTTPStatus

import alexandria_client.util as util
from alexandria_client.alexandria_endpoint import AlexandriaEndpoint
from alexandria_client.annotator import Annotator
from alexandria_client.rest_requester import RestRequester
from alexandria_client.state import *
from alexandria_client.state_prototype import *


class ResourcesEndpoint(AlexandriaEndpoint):
    endpoint = 'resources'
    state = 'state'

    def add(self, proto):
        def adder():
            return self.alexandria.post(self.endpoint, proto.entity)

        add_result = RestRequester(adder).on_status(HTTPStatus.CREATED, util.location_as_uuid).invoke()

        if self.alexandria.auto_confirm and not add_result.failed:
            self.confirm(add_result.uuid)

        return add_result

    def confirm(self, uuid):
        def confirm():
            uri = self.resource_state_uri(uuid)
            data = StatePrototype(State.CONFIRMED).entity
            return self.alexandria.put(uri=uri, data=data)

        return RestRequester(confirm).on_status(HTTPStatus.NO_CONTENT, util.response_as_is).invoke()

    def get(self, uuid):
        def getter():
            return self.alexandria.get(util.endpoint_uri(self.endpoint, uuid))

        return RestRequester(getter).on_status(HTTPStatus.OK, util.entity_as_json).invoke()

    def set(self, uuid, proto):
        def updater():
            return self.alexandria.put(uri=util.endpoint_uri(self.endpoint, uuid), data=proto.entity)

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
            return self.alexandria.put_data(uri=util.endpoint_uri(self.endpoint, uuid, 'text'), data=xml)

        def status_getter():
            return self.alexandria.get(uri=util.endpoint_uri(self.endpoint, uuid, 'text', 'status'))

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
            return self.alexandria.get(util.endpoint_uri(self.endpoint, uuid, 'text', 'xml'))

        return RestRequester(getter).on_status(HTTPStatus.OK, util.response_as_is).invoke().response.text

    def get_text_using_view(self, uuid, view_name):
        def getter():
            return self.alexandria.get(
                util.endpoint_uri(self.endpoint, uuid, 'text', 'xml') + "?view=" + view_name)

        return RestRequester(getter).on_status(HTTPStatus.OK, util.response_as_is).invoke().response.text

    def get_dot(self, uuid):
        def getter():
            return self.alexandria.get(util.endpoint_uri(self.endpoint, uuid, 'text', 'dot'))

        return RestRequester(getter).on_status(HTTPStatus.OK, util.response_as_is).invoke().response.text

    def set_view(self, uuid, name, view):
        def updater():
            return self.alexandria.put(uri=util.endpoint_uri(self.endpoint, uuid, 'text', 'views', name),
                                       data=view.entity)

        return RestRequester(updater).on_status(HTTPStatus.OK, util.response_as_is).invoke().response.text

    def set_annotator(self, uuid, annotator):
        def updater():
            return self.alexandria.put(uri=util.endpoint_uri(self.endpoint, uuid, 'annotators', annotator.name),
                                       data=annotator.entity)

        return RestRequester(updater).on_status(HTTPStatus.OK, util.response_as_is).invoke().response.text

    def get_annotators(self, uuid):
        def getter():
            return self.alexandria.get(util.endpoint_uri(self.endpoint, uuid, 'annotators'))

        json = RestRequester(getter).on_status(HTTPStatus.OK, util.response_as_is).invoke().response.json()
        annotators = [Annotator(a['annotator']['code'], a['annotator']['description']) for a in json]
        return annotators
