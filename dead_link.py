from requests_html import HTMLSession
import requests
from sys import argv
from urllib.parse import urlparse, urljoin
DEBUG = True

USAGE = '''
USAGE:
python dead_link.py www.itest.info
'''

if len(argv) != 2:
  print(USAGE)
  exit(1)

script_name, url = argv 

if url[:4] != 'http':
  url = 'http://' + url

res = urlparse(url)
if res.netloc == '':
  print('无法获取站点的domain信息')
  exit(1)

domain = res.netloc
print(f"站点domain: {domain}")

session = HTMLSession()
r = session.get(url)

links = r.html.find('a')

for link in links:
  if 'href' in link.attrs:
    href = link.attrs['href']
  else:
    continue
  result = urlparse(href)
  if result.netloc == '':
    href = urljoin(url, href)
    url_type = '内链'
  else:
    if domain in href:
      url_type = '内链'
    else:
      url_type = '外链'
  try:
    response = requests.get(href)
    if response.status_code >= 400:
      print(f"{url_type} {href} 失败")
    else:
      print(f"{url_type} {href} 成功")
  except:
    print("出现异常")
  


