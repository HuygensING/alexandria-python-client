from alexandria_notebook.element import Element


class TextView:
    def __init__(self, name):
        self.name = name
        self.description = ""
        self.elements = []

    def description(self, description: str):
        self.description = description
        return self

    def add_element(self, element: Element):
        self.elements.append(element)
        return self

    def elements(self, elements):
        self.elements = elements
        return self
