class Annotator:
    """
    Someone who can make text annotations
    """

    def __init__(self, name, description=""):
        """
        :param name:
        :type str:
        :param description:
        :type str:
        """
        self.name = name
        self.description = description

    @property
    def entity(self):
        return {'annotator': {'description': self.description}}

    def __repr__(self):
        return "Annotator::" + self.name + " (" + self.description + ")"
