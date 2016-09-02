from alexandria_notebook.element import Element


class TextView:
    def __init__(self, name):
        self.name = name
        self.description = ""
        self.elements = []

    def __dir__(self):
        return ['name', 'description', 'elements']

    @property
    def entity(self):
        element_dict = {}
        for e in self.elements:
            element_dict[e.name] = {'elementMode': e.element_mode, 'attributeMode': e.attribute_mode}
        return {'textView': {'description': self.description, 'elements': element_dict}}
