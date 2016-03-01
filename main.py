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
    print(json.dumps(a8a.about()))

    uuid = a8a.register_resource("http://www.example.com/some/resource")
    res = a8a.get_resource(uuid=uuid)

    print(res)


if __name__ == "__main__":
    main(sys.argv[1:])
