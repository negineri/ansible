import argparse
import requests
import sys

parser = argparse.ArgumentParser(description='get pypi package version')
parser.add_argument('arg1', help='target package name')
args = parser.parse_args()

try:
    res = requests.get("https://pypi.org/pypi/" + args.arg1 + "/json")
except requests.exceptions.RequestException as err:
    print(err)
    sys.exit(1)

json_data = res.json()

if json_data['info']['version'] is None or json_data['info']['version'] == '':
    sys.exit(1)

official_version = json_data["info"]["version"]

current_version = ''
with open('version', mode='r') as f:
    current_version = f.readline()

if official_version == current_version:
    sys.exit(0)

with open('version', mode='w') as f:
    print(official_version)
    f.write(official_version)

# subprocess.run(['git', 'push', 'origin', 'master'], encoding='utf-8', stdout=subprocess.PIPE)
