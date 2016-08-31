import argparse
import sys
import uuid

from alexandria_client.alexandria import Alexandria, ResourcePrototype


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auth", dest="auth", help="Local authentication token")
    parser.add_argument("-k", "--key", dest="key_file", help='Client Certificate Private Key file')
    parser.add_argument("-c", "--cert", dest="cert_file", help='Client Certificate file')
    parser.add_argument("-s", "--server", dest="server", help='Base URI of Alexandria server')
    args = parser.parse_args(argv)
    print("ARGS:", args)

    alexandria = Alexandria(args.server, args.auth)
    about = alexandria.about().json
    assert about['scmBranch'] == 'develop'
    print("ABOUT:", about)

    resources = alexandria.resources

    res_id = resources.add(ResourcePrototype("http://www.example.com/some/resource")).uuid
    res = resources.get(res_id).json
    assert res['resource']['state']['value'] == 'CONFIRMED'
    print(res['resource']['state'])

    res = resources.set(res_id, ResourcePrototype("http://www.example.com/another/resource"))
    print("RES:", res)

    res = resources.get(res_id).json
    assert res['resource']['ref'] == "http://www.example.com/another/resource"
    print(res)

    random_id = uuid.uuid4()
    res = resources.set(random_id, ResourcePrototype("http://www.example.com/somewhere/else"))
    print("RES:", res)


if __name__ == "__main__":
    main(sys.argv[1:])
