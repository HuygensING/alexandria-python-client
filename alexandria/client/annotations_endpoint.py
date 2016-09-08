from alexandria.client.alexandria_endpoint import AlexandriaEndpoint


class AnnotationsEndpoint(AlexandriaEndpoint):
    endpoint = 'annotations'

    def __call__(self):
        return self.get()

    def post(self, query):
        def getter():
            return self.alexandria.get(self.endpoint)

        return self.alexandria.post(self.endpoint, query.entity)
