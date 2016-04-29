import urllib3
import xml.etree.ElementTree as ET
import re
import time

http = urllib3.PoolManager()

def getSearchUrls(baseUrl):
    listOfUrls = [baseUrl]
    
    r = http.request('get', baseUrl)
    #root = ET.fromstring(r.data)
    #maxOffset
    start = r.data.index('Found')
    foundNum = r.data[start: start + 20].split()[1]
    maxOffset = int(foundNum) / 10
    listOfUrls += [baseUrl+"&offset="+str((x+1)*10) for x in xrange(maxOffset)] 
    return listOfUrls, int(foundNum)


def getPropertyUrls(filterStr="", exclude=True):
    result = []
    statusCount = {'ok': 0, 'err': 0}
    allSearchPages, foundNum = getSearchUrls('http://www.daft.ie/dublin/apartments-for-rent/?s%5Bmxp%5D=1500&s%5Bignored_agents%5D%5B0%5D=5732&s%5Bignored_agents%5D%5B1%5D=428&s%5Bignored_agents%5D%5B2%5D=1551')

    print "total properties from base url: ", foundNum
    print 'filtering...'
    remainingProperties = foundNum
    for page in allSearchPages:
        start = 0
        r = http.request('get', page)
        propertiesOnPage = 10 if remainingProperties >= 10 else remainingProperties
        for x in xrange(propertiesOnPage):
            start = r.data.index('sr_counter', start+1)
            tagStart = r.data.index('<a', start)
            quoteStart = r.data.index('"', tagStart)
            quoteEnd = r.data.index('"', quoteStart+1)
            path = r.data[quoteStart+1: quoteEnd+1]
            link = "http://www.daft.ie" + path
#            print link
            propertyResp = http.request('get', link)
            if propertyResp.status == 200:
                statusCount['ok'] += 1
                if len(filterStr) > 0:
                    result += [link]
                else:
                    result += [link]
            else:
                statusCount['err'] += 1 
        remainingProperties -= 10
    return result, statusCount
t1 = time.time()
urls, statusCount = getPropertyUrls()
t2 = time.time()
print 'results:'
print 'status count:'
print '    ok  - ', statusCount['ok']
print '    err - ', statusCount['err']
print 'time taken', t2 - t1

#for url in urls:
#    print url

#find by sr_couter

#p = re.compile('minimum 3 months')
#
#for item in root.iter('item'):
#    print 'item:', "".join(item.itertext())
#print p.search(root.text.lower())


