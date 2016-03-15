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
    about = a8a.about().cargo
    assert about['scmBranch'] == 'develop'
    print(about)

    uuid = a8a.add_resource(alexandria.ResourcePrototype("http://www.example.com/some/resource")).cargo
    res = a8a.get_resource(uuid).cargo
    assert res['resource']['state']['value'] == 'CONFIRMED'
    print(res['resource']['state'])

    a8a.set_resource(uuid, alexandria.ResourcePrototype("http://www.example.com/another/resource"))
    res = a8a.get_resource(uuid).cargo
    assert res['resource']['ref'] == "http://www.example.com/another/resource"
    print(res)


if __name__ == "__main__":
    main(sys.argv[1:])
