class StatePrototype:
    def __init__(self, state):
        self.state = state.name

    @property
    def entity(self):
        return self.__dict__
