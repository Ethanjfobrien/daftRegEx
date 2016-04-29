import urllib3
import xml.etree.ElementTree as ET
import re

http = urllib3.PoolManager()
r = http.request('get', 'http://www.daft.ie/dublin/apartments-for-rent/chapelizod/knockmaree-st-laurence-road-chapelizod-dublin-1639870/')
#root = ET.fromstring(r.data)

p = re.compile('minimum 3 months')

print p.search(r.data.lower())


