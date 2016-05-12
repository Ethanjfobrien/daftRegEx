import urllib3
import xml.etree.ElementTree as ET
import re
import time
import os
import sqlite3
import sys

http = urllib3.PoolManager()
user_agent = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F'}
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
        r = http.request('get', page, headers=user_agent)
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
                    isMatch = False
                    data = propertyResp.data.lower()
                    for s in filterStr:
                        if data.find(s.lower()) >= 0:
                            isMatch = True
                    if not isMatch : 
                        
                        boxStart = r.data.rfind('<div class="box', 0, start)
                        boxEnd = r.data.find('saved ads', boxStart)
                        boxEnd = r.data.find('</div', boxEnd)
                        boxEnd = r.data.find('</div', boxEnd+1)
                        box = r.data[boxStart: boxEnd+6]
                        result += [(link, box.replace('<a href="', '<a href="http://www.daft.ie'))]
                else:
                    result += [(link, "")]
            else:
                statusCount['err'] += 1 
        remainingProperties -= 10
    return result, statusCount


t1 = time.time()
urls, statusCount = getPropertyUrls(['Minimum 1 Year', 'Minimum 6 Months', 'minimum 9 months'])
t2 = time.time()
print 'results:'
print 'num of urls: ', len(urls)
print 'status count:'
print '    ok  - ', statusCount['ok']
print '    err - ', statusCount['err']
print 'time taken', t2 - t1
print 'writing ....'
filename = 'build/index.html'
try:
    os.remove(filename)
except OSError:
    pass
with open(filename, 'w') as f:
    f.write('''
<!DOCTYPE html>
<head>
<title>Test</title>
<link rel="stylesheet"
              type="text/css"
              href="daft.ie.css" />
</head>
<body>
<table id="sr_content">
<tbody>
<tr>
<td style="vertical-align:top">
    ''')
    for url in urls:
        if not len(url[1]) > 0:
            f.write('<a href="')
            f.write(url[0])
            f.write('">'+url[0]+'</a><br>\n')
        else:
            f.write(url[1])
    f.write('''
</td >
</tr>
</tbody>
</table>
</body>
    ''')
print 'all urls written.'

#find by sr_couter

#p = re.compile('minimum 3 months')
#
#for item in root.iter('item'):
#    print 'item:', "".join(item.itertext())
#print p.search(root.text.lower())


