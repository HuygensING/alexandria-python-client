from enum import Enum
from http import HTTPStatus
from urllib.parse import urljoin

import requests

from rest_requester import RestRequester
from rest_result import RestResult


class AlexandriaEndpoint:
    def __init__(self, alexandria):
        self.alexandria = alexandria


class AboutEndpoint(AlexandriaEndpoint):
    endpoint = 'about'

    def __call__(self):
        return self.get()

    def get(self):
        def getter():
            return self.alexandria.get(self.endpoint)

        return RestRequester(getter).on_status(HTTPStatus.OK, entity_as_json).invoke()


class ResourcesEndpoint(AlexandriaEndpoint):
    endpoint = 'resources'
    state = 'state'

    def add(self, proto):
        def adder():
            return self.alexandria.post(self.endpoint, proto.entity)

        add_result = RestRequester(adder).on_status(HTTPStatus.CREATED, location_as_uuid).invoke()

        if self.alexandria.auto_confirm and not add_result.failed:
            self.confirm(add_result.uuid)

        return add_result

    def confirm(self, uuid):
        def confirm():
            uri = self.resource_state_uri(uuid)
            data = StatePrototype(State.CONFIRMED).entity
            return self.alexandria.put(uri=uri, data=data)

        return RestRequester(confirm).on_status(HTTPStatus.NO_CONTENT, response_as_is).invoke()

    def get(self, uuid):
        def getter():
            return self.alexandria.get(endpoint_uri(self.endpoint, uuid))

        return RestRequester(getter).on_status(HTTPStatus.OK, entity_as_json).invoke()

    def set(self, uuid, proto):
        def updater():
            return self.alexandria.put(uri=endpoint_uri(self.endpoint, uuid), data=proto.entity)

        return RestRequester(updater) \
            .on_status(HTTPStatus.OK, entity_as_json) \
            .on_status(HTTPStatus.CREATED, location_as_uuid) \
            .on_status(HTTPStatus.NO_CONTENT, response_as_is) \
            .invoke()

    def resource_uri(self, uuid):
        return endpoint_uri(self.endpoint, uuid)

    def resource_state_uri(self, uuid):
        return endpoint_uri(self.endpoint, uuid, self.state)


class Alexandria:
    def __init__(self, server, auth, auto_confirm=True):
        self.server = server if server.endswith('/') else server + '/'
        self.session = requests.Session()
        self.session.headers['x-ssl-client-s-dn-cn'] = auth
        self.auto_confirm = auto_confirm
        self.about = AboutEndpoint(self)
        self.resources = ResourcesEndpoint(self)

    def get(self, uri):
        url = urljoin(self.server, uri)
        r = self.session.get(url=url)
        r.raise_for_status()
        return r

    def put(self, uri, data):
        url = urljoin(self.server, uri)
        r = self.session.put(url=url, json=data)
        r.raise_for_status()
        return r

    def post(self, uri, data):
        url = urljoin(self.server, uri)
        r = self.session.post(url=url, json=data)
        r.raise_for_status()
        return r

    def delete(self, uri):
        r = self.session.delete(url=urljoin(self.server, uri))
        r.raise_for_status()
        return r


def entity_as_json(response):
    return RestResult(json=response.json())


def location_as_uuid(response):
    return RestResult(uuid=response.headers['location'].split('/')[-1])


def response_as_is(response):
    return RestResult(response=response)


def endpoint_uri(*args):
    return "/".join(map(str, args))


class ResourcePrototype:
    def __init__(self, ref):
        self.ref = ref

    @property
    def entity(self):
        return {'resource': self.__dict__}


class StatePrototype:
    def __init__(self, state):
        self.state = state.name

    @property
    def entity(self):
        return self.__dict__


class State(Enum):
    TENTATIVE = 0
    CONFIRMED = 1
    DELETED = 2
    DEPRECATED = 3

    def __str__(self):
        return self.name
