import sys
import pydot

from IPython.display import Image, display

from alexandria_client.alexandria import Alexandria


class ResourceProxy:
    def __init__(self, resource_id: str, uuid: str, alexandria: Alexandria):
        self.id = resource_id
        self.uuid = uuid
        self.resources = alexandria.resources

    def __dir__(self):
        return ['id', 'uuid', 'set_xml', 'get_xml', 'export_dot', 'show_graph', 'set_view']

    def set_xml(self, xml):
        self.resources.set_text(self.uuid, xml)

    def get_xml(self):
        return self.resources.get_text(self.uuid)

    def get_xml_using_view(self, view_name):
        return self.resources.get_text_using_view(self.uuid, view_name)

    def export_dot(self):
        return self.resources.get_dot(self.uuid)

    def show_graph(self):
        dot = self.export_dot()
        graphs = pydot.graph_from_dot_data(dot)
        (g,) = graphs
        png_data = g.create(format='png')
        png = Image(png_data)
        display(png)

    def set_view(self, text_view):
        self.resources.set_view(self.uuid, text_view.name, text_view)

    def __str__(self):
        return "ResourceProxy::" + self.id
