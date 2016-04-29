import urllib3
import xml.etree.ElementTree as ET
import re

http = urllib3.PoolManager()

def getListOfUrls(baseUrl):
    listOfUrls = [baseUrl]
    
    r = http.request('get', baseUrl)
    #root = ET.fromstring(r.data)
    #maxOffset
    start = r.data.index('Found')
    foundNum = r.data[start: start + 20].split()[1]
    maxOffset = int(foundNum) / 10
    listOfUrls += [baseUrl+"&offset="+str((x+1)*10) for x in xrange(maxOffset)] 
    return listOfUrls

print getListOfUrls('http://www.daft.ie/dublin/apartments-for-rent/?s%5Bmxp%5D=1500&s%5Bignored_agents%5D%5B0%5D=5732&s%5Bignored_agents%5D%5B1%5D=428&s%5Bignored_agents%5D%5B2%5D=1551')

#find by sr_couter

#p = re.compile('minimum 3 months')
#
#for item in root.iter('item'):
#    print 'item:', "".join(item.itertext())
#print p.search(root.text.lower())


