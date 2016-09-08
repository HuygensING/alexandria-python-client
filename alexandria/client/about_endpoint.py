from http import HTTPStatus

import alexandria.client.util as util
from alexandria.client.rest_requester import RestRequester

from alexandria.client.alexandria_endpoint import AlexandriaEndpoint


class AboutEndpoint(AlexandriaEndpoint):
    endpoint = 'about'

    def __call__(self):
        return self.get()

    def get(self):
        def getter():
            return self.alexandria.get(self.endpoint)

        return RestRequester(getter).on_status(HTTPStatus.OK, util.entity_as_json).invoke()
