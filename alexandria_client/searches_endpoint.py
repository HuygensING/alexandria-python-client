from alexandria_client.alexandria_endpoint import AlexandriaEndpoint


class SearchesEndpoint(AlexandriaEndpoint):
    endpoint = 'searches'

    # def __call__(self):
    #     return self.get()

    def post(self, query):
        def getter():
            return self.alexandria.get(self.endpoint)

        return self.alexandria.post(self.endpoint, query.entity)
