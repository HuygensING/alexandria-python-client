from alexandria_client.rest_result import RestResult


def entity_as_json(response):
    return RestResult(json=response.json())


def location_as_uuid(response):
    return RestResult(uuid=response.headers['location'].split('/')[-1])


def response_as_is(response):
    return RestResult(response=response)


def endpoint_uri(*args):
    return "/".join(map(str, args))
