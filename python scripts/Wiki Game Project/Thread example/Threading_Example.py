from urlparse import urlparse
import httplib, sys, threading, Queue, time
sys.path.append('C:\Python27\Lib\profilehooks-1.7')
from profilehooks import timecall

MAX_LINKS=10000000
NUM_OF_THREADS=32
q=Queue.Queue()
       
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
    #if status==200:
    #    print "status 200"
    if status!=200:
        print 'status: {}, url: {}'.format(status, url)      


def doWork():
    while True:
        url=q.get()
        status,url=getStatus(url)
        doSomethingWithResult(status,url)
        q.task_done()
        
@timecall(immediate=True)
def Main_Func():   
    for i in xrange(NUM_OF_THREADS):
        t = threading.Thread(target=doWork)
        t.daemon = True
        t.start()

    for url in open('urllist.txt'):
        q.put(url)
    q.join()
    print "BB"
    print q.empty()
    for url in open('urllist.txt'):
        q.put(url)
    q.join()
    
for i in xrange(2):
    Main_Func()
    
