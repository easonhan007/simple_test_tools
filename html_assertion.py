from requests_html import HTMLSession
from sys import argv
DEBUG = True

USAGE = '''
USAGE:
python html_assertion.py www.itest.info .thumbnail-img 4
'''

if len(argv) != 4:
  print(USAGE)
  exit(1)

script_name, url, css_selector, length = argv

if url[:4] != 'http':
  url = 'http://' + url

session = HTMLSession()
r = session.get(url)

elements = r.html.find(css_selector)


def debug():
  if DEBUG:
    print('*' * 100)
    print(f"css选择器: {css_selector}, 共找到{len(elements)}个元素\n")
    for element in elements:
      print(element.html)
      print(element.attrs)
      print()


if len(elements) != int(length):
  print(f"失败! 预期{length}个元素，实际存在{len(elements)}个元素\n")
  debug()
  exit(1)
else:
  print(f"成功!\n")
  debug()
