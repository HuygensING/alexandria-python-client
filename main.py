import alexandria
import argparse
import json
import sys


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auth", dest="auth", help="Local authentication token")
    parser.add_argument("-k", "--key", dest="key_file", help='Client Certificate Private Key file')
    parser.add_argument("-c", "--cert", dest="cert_file", help='Client Certificate file')
    parser.add_argument("-s", "--server", dest="server", help='Base URI of Alexandria server')
    args = parser.parse_args(argv)
    print(args)

    a8a = alexandria.Alexandria(args.server, args.auth)
    r = a8a.about()
    result = r.json()
    print(json.dumps(result))

    # a8a.register_resource("http://www.example.com/some/resource")
    uuid = a8a.register_resource("http://www.example.com/bogus/resource", "d224ff81-b26f-4fce-a54f-56c74f6819d6")

    res = a8a.get_resource(uuid)
    print(res)


if __name__ == "__main__":
    main(sys.argv[1:])
