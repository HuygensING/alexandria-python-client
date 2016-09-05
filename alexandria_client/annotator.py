class Annotator:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description

    @property
    def entity(self):
        return {'annotator': {'description': self.description}}

    def __repr__(self):
        return "Annotator::" + self.name + " (" + self.description + ")"
