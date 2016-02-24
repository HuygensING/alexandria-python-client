import requests

_server = 'http://tc23.huygens.knaw.nl/test-alexandria'


def about(server=_server):
    r = requests.get(server + "/about", timeout=5.0)
    return r
