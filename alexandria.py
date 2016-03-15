from enum import Enum
from http import HTTPStatus
from urllib.parse import urljoin

import requests

from rest_requester import RestRequester
from rest_result import RestResult


class Alexandria:
    def __init__(self, server, auth, auto_confirm=True):
        self.server = server if server.endswith('/') else server + '/'
        self.session = requests.Session()
        self.session.headers['x-ssl-client-s-dn-cn'] = auth
        self.auto_confirm = auto_confirm

    def about(self):
        def getter():
            return self.get(endpoint_uri(Endpoint.ABOUT))

        return RestRequester(getter).on_status(HTTPStatus.OK, entity_as_cargo).invoke()

    def add_resource(self, proto):
        def adder():
            return self.post(endpoint_uri(Endpoint.RESOURCES), proto.entity)

        add_result = RestRequester(adder).on_status(HTTPStatus.CREATED, location_as_cargo).invoke()

        if self.auto_confirm and not add_result.failed:
            self.confirm_resource(add_result.cargo)

        return add_result

    def get_resource(self, uuid):
        def getter():
            return self.get(endpoint_uri(Endpoint.RESOURCES, uuid))

        return RestRequester(getter).on_status(HTTPStatus.OK, entity_as_cargo).invoke()

    def set_resource(self, uuid, proto):
        def updater():
            return self.put(endpoint_uri(Endpoint.RESOURCES, uuid), proto.entity)

        return RestRequester(updater) \
            .on_status(HTTPStatus.OK, entity_as_cargo) \
            .on_status(HTTPStatus.CREATED, location_as_cargo) \
            .on_status(HTTPStatus.NO_CONTENT, response_as_is) \
            .invoke()

    def confirm_resource(self, uuid):
        def confirm():
            uri = endpoint_uri(Endpoint.RESOURCES, uuid, "state")
            data = StatePrototype(State.CONFIRMED).entity
            return self.put(uri=uri, data=data)

        return RestRequester(confirm).on_status(HTTPStatus.NO_CONTENT, response_as_is).invoke()

    def get(self, uri):
        url = urljoin(self.server, uri)
        return self.session.get(url=url)

    def put(self, uri, data):
        url = urljoin(self.server, uri)
        return self.session.put(url=url, json=data)

    def post(self, uri, data):
        url = urljoin(self.server, uri)
        return self.session.post(url=url, json=data)

    def delete(self, uri):
        return self.session.delete(url=urljoin(self.server, uri))


def response_as_is(response):
    return RestResult(response=response)


def entity_as_cargo(response):
    return RestResult(cargo=response.json())


def endpoint_uri(*args):
    return "/".join(map(str, args))


def location_as_cargo(response):
    return RestResult(cargo=response.headers['location'].split('/')[-1])


class Prototype:
    def entity(self, wrapper=None):
        return {wrapper: self.__dict__} if wrapper else self.__dict__


class ResourcePrototype(Prototype):
    def __init__(self, ref):
        self.ref = ref

    @property
    def entity(self):
        return super().entity('resource')


class StatePrototype(Prototype):
    def __init__(self, state):
        self.state = state.name

    @property
    def entity(self):
        return super().entity()


class State(Enum):
    TENTATIVE = 0
    CONFIRMED = 1
    DELETED = 2
    DEPRECATED = 3

    def __str__(self):
        return self.name


class Endpoint(Enum):
    ABOUT = '/about'
    RESOURCES = '/resources'

    def __str__(self):
        return self.name.lower()
