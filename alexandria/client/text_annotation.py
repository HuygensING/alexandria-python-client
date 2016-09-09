class TextAnnotation:
    def __init__(self, name, annotator_id, position, attributes=None):
        self.name = name
        self.annotator = annotator_id
        self.position = position
        self.attributes = attributes

    @property
    def entity(self):
        position = {'xml:id': self.position.xml_id}
        if self.position.offset is not None:
            position['offset'] = self.position.offset
            position['length'] = self.position.length
        annotation = {'name': self.name, 'annotator': self.annotator,
                      'position': position}
        if self.attributes is not None:
            annotation['attributes'] = self.attributes
        entity = {
            'textAnnotation': annotation}
        return entity
