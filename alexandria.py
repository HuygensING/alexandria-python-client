import requests


class Alexandria:
    def __init__(self, server, auth):
        self.server = server
        self.auth = auth

    def endpoint_url(self, endpoint):
        return self.server + "/" + endpoint

    def about(self):
        r = self.__get("about")
        if r.status_code == 200:
            return r.json()
        self.__raise(r, "Failed to get: " + r.url)

    def get_resource(self, uuid):
        print("UUID:", uuid)
        endpoint = "resources/" + uuid
        return self.__get(endpoint=endpoint).json()

    def register_resource(self, uri):
        payload = {'resource': {'ref': uri}}

        r = self.__post(endpoint="resources", payload=payload)
        if r.status_code == 201:  # Created
            return r.headers['location'].split('/')[-1]

        self.__raise(r, "Failed to register resource: " + r.url)

    def __get(self, endpoint):
        return self.__request(method='get', endpoint=endpoint)

    def __put(self, endpoint, payload):
        return self.__request(method='put', endpoint=endpoint, payload=payload)

    def __post(self, endpoint, payload):
        return self.__request(method='post', endpoint=endpoint, payload=payload)

    def __delete(self, endpoint):
        return self.__request(method='delete', endpoint=endpoint)

    def __request(self, method, endpoint, payload=None):
        url = self.endpoint_url(endpoint)
        headers = {'x-ssl-client-s-dn-cn': self.auth}
        return requests.request(method=method, url=url, headers=headers, json=payload)

    @staticmethod
    def __raise(r, message=None):
        try:
            detail = r.json()['error']['message']
        except ValueError:
            detail = r

        print("URL:", r.url)
        if message is None:
            raise Exception(r.status_code, detail)
        else:
            raise Exception(message, r.status_code, detail)
