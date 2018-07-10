import requests
from sys import argv

USAGE = '''
USAGE:
python get.py https://api.github.com
'''

if len(argv) != 2:
  print(USAGE)
  exit()

script_name, url = argv

if url[:3] != 'http':
  url = 'http://' + url

r = requests.get(url)

print(f"接口地址: {url}\n")
print(f"状态码: {r.status_code}\n")
print(f"Headers:")
for key, value in r.headers.items():
  print(f"{key} : {value}")

print(r.text)
