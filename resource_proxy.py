import sys


class ResourceProxy:
    def __init__(self, resource_id, alexandria):
        self.id = resource_id
        self.client = alexandria

    def set_xml(self, xml):
        print("TODO:set_xml")

    def get_xml(self):
        print("TODO:get_xml")

    def export_dot(self):
        print("TODO:" + sys._getframe().f_code.co_name)

    def __str__(self):
        return "ResourceProxy::" + self.id
