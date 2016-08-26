from alexandria import Alexandria
from resource_proxy import ResourceProxy


class AlexandriaProxy:
    def __init__(self, server_url):
        self.client = Alexandria(server_url)

    def create_resource(self, resource_id):
        rp = ResourceProxy(resource_id, self.client)
        return rp

    def get_resource(self, resource_id):
        rp = ResourceProxy(resource_id, self.client)
        return rp
