from alexandria import *
from resource_proxy import *


class AlexandriaProxy:
    def __init__(self, server_url, admin_key):
        self.alexandria = Alexandria(server_url, admin_key=admin_key)

    def create_resource(self, resource_id):
        uuid = self.alexandria.resources.add(ResourcePrototype(resource_id)).uuid
        rp = ResourceProxy(resource_id, uuid, self.alexandria)
        return rp

    def get_resource(self, resource_id):
        uuid = ''
        rp = ResourceProxy(resource_id, uuid, self.alexandria)
        return rp
