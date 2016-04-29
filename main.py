import urllib3
import xml.etree.ElementTree as ET
import re

http = urllib3.PoolManager()
r = http.request('get', 'http://httpbin.org/html')
root = ET.fromstring(r.data)

p = re.compile('h')

print p.search(root[1][0].text.lower())


