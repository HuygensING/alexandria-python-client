import time
from http import HTTPStatus
from urllib.parse import urljoin

import requests

import alexandria.client.util as util
from alexandria.client.about_endpoint import AboutEndpoint
from alexandria.client.annotations_endpoint import AnnotationsEndpoint
from alexandria.client.resources_endpoint import ResourcesEndpoint
from alexandria.client.rest_requester import RestRequester


class Alexandria:
    def __init__(self, server, admin_key="", auth="", auto_confirm=True):
        self.server = server if server.endswith('/') else server + '/'
        self.session = requests.Session()
        self.session.headers['x-ssl-client-s-dn-cn'] = auth
        self.session.headers['auth'] = 'SimpleAuth ' + admin_key
        self.session.headers['content-type'] = 'application/json'
        self.auto_confirm = auto_confirm
        self.about = AboutEndpoint(self)
        self.resources = ResourcesEndpoint(self)
        # self.searches = SearchesEndpoint(self)
        self.annotations = AnnotationsEndpoint(self)

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

    def put_data(self, uri, data):
        url = urljoin(self.server, uri)
        current_content_type = self.session.headers.get('content-type')
        self.session.headers['content-type'] = 'text/xml'
        r = self.session.put(url=url, data=data)
        self.session.headers['content-type'] = current_content_type
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

    def do_xpath(self, resource_view_ids, xpath):
        entity = {
            'resourceIds': resource_view_ids,
            'xpath': xpath
        }

        def poster():
            return self.post(util.endpoint_uri('commands', 'xpath'), entity)

        def status_getter():
            return self.alexandria.get(uri=util.endpoint_uri(self.endpoint, uuid, 'text', 'status'))

        return RestRequester(poster).on_status(HTTPStatus.OK, util.entity_as_json).invoke().json

    def aql2(self, aql2_command):
        entity = {'command': aql2_command}

        def poster():
            return self.post(util.endpoint_uri('commands', 'aql2'), entity)

        response = RestRequester(poster).on_status(HTTPStatus.OK, util.response_as_is).invoke().response
        status_uri = response.headers['location']

        def status_getter():
            return self.get(uri=status_uri)

        done = False
        while not done:
            time.sleep(1)
            status = RestRequester(status_getter) \
                .on_status(HTTPStatus.OK, util.entity_as_json) \
                .invoke().json
            done = status['commandStatus']['done']

        return status
