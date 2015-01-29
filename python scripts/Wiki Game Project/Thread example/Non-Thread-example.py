from urlparse import urlparse
import httplib, sys
sys.path.append('C:\Python27\Lib\profilehooks-1.7')
from profilehooks import timecall

def getStatus(ourl):
    try:
        url = urlparse(ourl)
        conn = httplib.HTTPConnection(url.netloc)   
        conn.request("HEAD", url.path)
        res = conn.getresponse()
        return res.status, ourl
    except:
        return "error", ourl

def doSomethingWithResult(status, url):
    if status!=200:
        print 'status: {}, url: {}\n'.format(status, url)

@timecall(immediate=True)
def checkStatus():
    for url in open('urllist.txt'):
        status,url=getStatus(url)
        doSomethingWithResult(status,url)        

checkStatus()
