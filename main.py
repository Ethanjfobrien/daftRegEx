import urllib3
import xml.etree.ElementTree as ET
import re
import time
import os
import sqlite3

http = urllib3.PoolManager()
#conn = sqlite3.connect('main.db')
#c = conn.cursor()

#c.execute('''create table if not exists urls(url varchar(100) primary key, timestamp int) ''')

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
            path = r.data[quoteStart+1: quoteEnd]
            link = "http://www.daft.ie" + path
#            print link
            propertyResp = http.request('get', link)
            if propertyResp.status == 200:
                statusCount['ok'] += 1
                if len(filterStr) > 0:
                    isMatch = propertyResp.data.lower().find(filterStr.lower()) >= 0
                    if not isMatch : 
                        result += [link]
                else:
                    result += [link]
            else:
                statusCount['err'] += 1 
        remainingProperties -= 10
    return result, statusCount


t1 = time.time()
urls, statusCount = getPropertyUrls('Minimum 1 Year')
t2 = time.time()
print 'results:'
print 'status count:'
print '    ok  - ', statusCount['ok']
print '    err - ', statusCount['err']
print 'time taken', t2 - t1
print 'writing ....'
filename = 'urls.txt'
try:
    os.remove(filename)
except OSError:
    pass
with open(filename, 'w') as f:
    for url in urls:
        f.write(url)
        f.write('\n')
print 'all urls written to urls.txt'

#find by sr_couter

#p = re.compile('minimum 3 months')
#
#for item in root.iter('item'):
#    print 'item:', "".join(item.itertext())
#print p.search(root.text.lower())


