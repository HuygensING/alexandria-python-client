from urllib.parse import urljoin

import requests
from alexandria.about_endpoint import AboutEndpoint
from alexandria.annotations_endpoint import AnnotationsEndpoint
from alexandria.searches_endpoint import SearchesEndpoint

from alexandria.client.resources_endpoint import ResourcesEndpoint


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
        self.searches = SearchesEndpoint(self)
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
