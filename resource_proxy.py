import sys
from IPython.display import Image, display
import pydot

class ResourceProxy:
    def __init__(self, resource_id, uuid, alexandria):
        self.id = resource_id
        self.uuid = uuid
        self.resources = alexandria.resources

    def set_xml(self, xml):
        self.resources.set_text(self.uuid, xml)

    def get_xml(self):
        return self.resources.get_text(self.uuid)

    def export_dot(self):
        return self.resources.get_dot(self.uuid)

    def show_graph(self):
        dot = self.export_dot()
        graphs = pydot.graph_from_dot_data(dot)
        (g,) = graphs
        png_data = g.create(format='png')
        png = Image(png_data)
        display(png)

    def __str__(self):
        return "ResourceProxy::" + self.id
