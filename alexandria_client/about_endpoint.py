from http import HTTPStatus

import alexandria_client.util as util

from alexandria_client.alexandria_endpoint import AlexandriaEndpoint
from alexandria_client.rest_requester import RestRequester


class AboutEndpoint(AlexandriaEndpoint):
    endpoint = 'about'

    def __call__(self):
        return self.get()

    def get(self):
        def getter():
            return self.alexandria.get(self.endpoint)

        return RestRequester(getter).on_status(HTTPStatus.OK, util.entity_as_json).invoke()
