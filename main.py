import argparse
import requests
import sys
import re

pattern = r'^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'

parser = argparse.ArgumentParser(description='get pypi package version')
parser.add_argument('arg1', help='target package name')
args = parser.parse_args()

try:
    res = requests.get("https://pypi.org/pypi/" + args.arg1 + "/json")
except requests.exceptions.RequestException as err:
    print(err, file=sys.stderr)
    sys.exit(1)

json_data = res.json()

if json_data['info']['version'] is None or json_data['info']['version'] == '':
    sys.exit(1)

official_version = json_data["info"]["version"]

if re.match(pattern, official_version) is None:
    print("version is not semver.", file=sys.stderr)
    sys.exit(1)

current_version = ''
with open('version', mode='r') as f:
    current_version = f.readline()

if official_version == current_version:
    sys.exit(0)

with open('version', mode='w') as f:
    print(official_version)
    f.write(official_version)
