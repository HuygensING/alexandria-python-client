import json
import requests


class Alexandria:
    def __init__(self, server, auth):
        self.server = server
        self.auth = auth

    def about(self):
        r = requests.get(self.server + "/about", timeout=5.0)
        return r

    def get_resource(self, uuid):
        return self.__get("/resources/" + uuid).json()

    def register_resource(self, uri, uuid=None):
        payload = {'resource': {'ref': uri}}

        if uuid is None:
            r = self.__post("/resources", payload)
            if r.status_code == 201:  # Created
                location = r.headers['location']
                return location.split('/')[-1]
        else:
            r = self.__put("/resources/" + uuid, payload)
            if r.status_code == 204:  # No Content
                return uuid

        raise Exception("Failed to register resource", r.status_code, r.json()['error']['message'])

    def __get(self, endpoint):
        return self.__request(method='get', endpoint=endpoint)

    def __put(self, endpoint, payload):
        return self.__request(method='put', endpoint=endpoint, payload=payload)

    def __post(self, endpoint, payload):
        return self.__request(method='post', endpoint=endpoint, payload=payload)

    def __delete(self, endpoint):
        return self.__request(method='delete', endpoint=endpoint)

    def __request(self, method, endpoint, payload=None):
        url = self.server + endpoint
        headers = {'x-ssl-client-s-dn-cn': self.auth}
        return requests.request(method=method, url=url, headers=headers, json=payload)
