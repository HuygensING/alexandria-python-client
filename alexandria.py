from enum import Enum
from http import HTTPStatus
from urllib.parse import urljoin

import requests

from rest_requester import RestRequester
from rest_result import RestResult


class Alexandria:
    def __init__(self, server, auth, auto_confirm=True):
        self.server = server if server.endswith('/') else server + '/'
        self.auth = auth
        self.auto_confirm = auto_confirm

    def about(self):
        def getter():
            return self.__get(endpoint_uri(Endpoint.ABOUT))

        return RestRequester(getter).on_status(HTTPStatus.OK, ok).invoke()

    def add_resource(self, proto):
        def adder():
            return self.__post(endpoint_uri(Endpoint.RESOURCES), proto.entity)

        add_result = RestRequester(adder).on_status(HTTPStatus.CREATED, extract_uuid).invoke()

        if self.auto_confirm and not add_result.failed:
            self.confirm_resource(add_result.cargo)

        return add_result

    def get_resource(self, uuid):
        def getter():
            return self.__get(endpoint_uri(Endpoint.RESOURCES, uuid))

        return RestRequester(getter).on_status(HTTPStatus.OK, ok).invoke()

    def set_resource(self, uuid, proto):
        def updater():
            return self.__put(endpoint_uri(Endpoint.RESOURCES, uuid), payload=proto.entity)

        return RestRequester(updater).on_status(HTTPStatus.CREATED, ok).invoke()

    def confirm_resource(self, uuid):
        def confirm():
            uri = endpoint_uri(Endpoint.RESOURCES, uuid, "state")
            payload = StatePrototype(State.CONFIRMED).entity
            return self.__put(uri=uri, payload=payload)

        return RestRequester(confirm).on_status(HTTPStatus.NO_CONTENT, lambda r: RestResult(response=r)).invoke()

    def __get(self, uri):
        return self.__request(method='get', uri=uri)

    def __put(self, uri, payload):
        return self.__request(method='put', uri=uri, payload=payload)

    def __post(self, uri, payload):
        return self.__request(method='post', uri=uri, payload=payload)

    def __delete(self, uri):
        return self.__request(method='delete', uri=uri)

    def __request(self, method, uri, payload=None):
        url = urljoin(self.server, uri.lower())
        headers = {'x-ssl-client-s-dn-cn': self.auth}
        response = requests.request(method=method, url=url, headers=headers, json=payload)
        return response


def endpoint_uri(*args):
    return "/".join(map(str, args))


def extract_uuid(response):
    return RestResult(cargo=response.headers['location'].split('/')[-1])


def ok(response):
    return RestResult(cargo=response.json())


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
