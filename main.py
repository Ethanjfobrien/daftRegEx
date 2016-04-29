import urllib3
import xml.etree.ElementTree as ET
import re

http = urllib3.PoolManager()
r = http.request('get', 'http://httpbin.org/xml')
root = ET.fromstring(r.data)

p = re.compile('minimum 3 months')

for item in root.iter('item'):
    print 'item:', "".join(item.itertext())
print p.search(root.text.lower())


