"""
   Copyright 2017 Huygens ING

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import argparse
import sys
import uuid

from antioch.client.resource_prototype import *

from antioch.client.antoioch import Antioch


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auth", dest="auth", help="Local authentication token")
    parser.add_argument("-k", "--key", dest="key_file", help='Client Certificate Private Key file')
    parser.add_argument("-c", "--cert", dest="cert_file", help='Client Certificate file')
    parser.add_argument("-s", "--server", dest="server", help='Base URI of Alexandria server')
    args = parser.parse_args(argv)
    print("ARGS:", args)

    alexandria = Antioch(args.server, args.auth)
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
