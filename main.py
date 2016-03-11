import argparse
import sys

import alexandria


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auth", dest="auth", help="Local authentication token")
    parser.add_argument("-k", "--key", dest="key_file", help='Client Certificate Private Key file')
    parser.add_argument("-c", "--cert", dest="cert_file", help='Client Certificate file')
    parser.add_argument("-s", "--server", dest="server", help='Base URI of Alexandria server')
    args = parser.parse_args(argv)
    print(args)

    a8a = alexandria.Alexandria(args.server, args.auth)
    print(a8a.about().cargo['buildDate'])

    uuid = a8a.add_resource(alexandria.ResourcePrototype("http://www.example.com/some/resource")).cargo

    print(a8a.get_resource(uuid).cargo)

    print(a8a.set_resource(uuid, alexandria.ResourcePrototype("http://www.example.com/another/resource")))

    print(a8a.get_resource(uuid).cargo)

if __name__ == "__main__":
    main(sys.argv[1:])
