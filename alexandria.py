from enum import Enum
from http import HTTPStatus

import requests

from rest_requester import RestRequester
from rest_result import RestResult


class Alexandria:
    def __init__(self, server, auth, auto_confirm=True):
        self.server = server
        self.auth = auth
        self.auto_confirm = auto_confirm

    def endpoint_url(self, endpoint):
        return self.server + "/" + endpoint

    def about(self):
        def getter():
            return self.__get("about")

        return RestRequester(getter).on_status(HTTPStatus.OK, ok).invoke()

    def add_resource(self, proto):
        def adder():
            return self.__post("resources", proto.entity())

        add_result = RestRequester(adder).on_status(HTTPStatus.CREATED, extract_uuid).invoke()

        if self.auto_confirm and not add_result.failed:
            self.confirm_resource(add_result.cargo)

        return add_result

    def get_resource(self, uuid):
        def getter():
            return self.__get("resources/" + uuid)

        return RestRequester(getter).on_status(HTTPStatus.OK, ok).invoke()

    def set_resource(self, uuid, proto):
        def updater():
            return self.__put(endpoint="resources/" + uuid, payload=proto.entity())

        return RestRequester(updater).on_status(HTTPStatus.CREATED, ok).invoke()

    def confirm_resource(self, uuid):
        def confirm():
            state = StatePrototype(AlexandriaState.CONFIRMED)
            return self.__put(endpoint="resources/" + uuid + "/state", payload=state.entity())

        return RestRequester(confirm).on_status(HTTPStatus.NO_CONTENT, lambda r: RestResult(response=r)).invoke()

    def __get(self, endpoint):
        return self.__request(method='get', endpoint=endpoint)

    def __put(self, endpoint, payload):
        print("endpoint:", endpoint)
        print("payload:", payload)
        return self.__request(method='put', endpoint=endpoint, payload=payload)

    def __post(self, endpoint, payload):
        return self.__request(method='post', endpoint=endpoint, payload=payload)

    def __delete(self, endpoint):
        return self.__request(method='delete', endpoint=endpoint)

    def __request(self, method, endpoint, payload=None):
        url = self.endpoint_url(endpoint)
        headers = {'x-ssl-client-s-dn-cn': self.auth}
        response = requests.request(method=method, url=url, headers=headers, json=payload)
        print("__request::Response:", response)
        return response


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

    def entity(self):
        return super().entity('resource')


class StatePrototype(Prototype):
    def __init__(self, state):
        self.state = state.name

    def entity(self):
        return super().entity()


AlexandriaState = Enum('AlexandriaState', 'TENTATIVE, CONFIRMED, DELETED, DEPRECATED')
