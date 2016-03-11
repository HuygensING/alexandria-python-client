from requests.packages.urllib3.exceptions import MaxRetryError

from rest_result import RestResult


class RestRequester:
    def __init__(self, response_supplier):
        self.status_mappers = {}
        self.response_supplier = response_supplier

    def on_status(self, status, func):
        self.status_mappers[status] = func
        return self

    def invoke(self):
        response = self.response_supplier()
        try:
            return self.status_mappers[response.status_code](response)
        except KeyError:
            return RestResult(failed=True, response=response)
