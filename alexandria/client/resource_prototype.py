class ResourcePrototype:
    def __init__(self, ref):
        self.ref = ref

    @property
    def entity(self):
        return {'resource': self.__dict__}
