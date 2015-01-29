import urllib2, sys, time, threading, Queue, httplib
sys.path.append('C:\Python27\Lib\profilehooks-1.7')
from profilehooks import profile, timecall

def Print_Info():
    """ Print_Info() --> None

    prints running information.
    """
    global Listed_Articles, steps
    print "Listed",len(Listed_Articles),"articles so far."
    print steps, "steps have been taken so far."
    print ('===')

def Starts_With_Quotation_marks(x):
    """ Starts_With_Quotation_marks(string) --> bool

        returns true if x starts with the char '"', else returns false.
    """
    return x.startswith('"')

def URL_Isolate(x):
    """ URL_Isolate(string) --> string

        returns a substring of x from the first index in which the char
        '"' appears to the next index in which the char '"' appears.
    """
    l=x.split('"')
    newX=l[1]
    return newX

def Is_Wiki_Article(URL):
    """ Is_Wiki_Article(string) --> bool

        returns true if URL matches the format of an article in the english
        version of wikipedia, else returns false.

    """
    return URL.startswith("http://en.wikipedia.org/wiki/") and not (URL.startswith("http://en.wikipedia.org/wiki/Special:")
                                                                    or URL.startswith("http://en.wikipedia.org/wiki/Talk:")
                                                                    or URL.startswith("http://en.wikipedia.org/wiki/Help:")
                                                                    or URL.startswith("http://en.wikipedia.org/wiki/Category:")
                                                                    or URL.startswith("http://en.wikipedia.org/wiki/Wikipedia:")
                                                                    or URL.startswith("http://en.wikipedia.org/wiki/Portal:")
                                                                    or URL.startswith("http://en.wikipedia.org/wiki/File:")
                                                                    or URL.startswith("http://en.wikipedia.org/wiki/User:")
                                                                    or URL.startswith("http://en.wikipedia.org/wiki/User_talk:")
                                                                    or URL.startswith("http://en.wikipedia.org/wiki/Template:")
                                                                    or URL.startswith("http://en.wikipedia.org/wiki/Template_talk:"))
#
def Validate (URL):
    """ Validate(URL) --> bool

    returns true once the URL that was given was validated as a real wikipedia page. it won't return anything untill
    said task is done.
    """
    if not Is_Wiki_Article(URL):
            print "{} is not a valid wikipedia page, please try again!".format(URL)
    else:
        try: #Testing to see if the page exists
            request=urllib2.Request(URL)
            response=urllib2.urlopen(request)
        except urllib2.HTTPError:
            print "{} is not a valid wikipedia page, please try again!".format(URL)
        else:
            return True

def Get_URLs (source):
    """ Get_URLs (source) --> tuple

        returns all the URLs found in the source page in a tuple
        """
    splitted=source.split("href=")
    filtered=filter(Starts_With_Quotation_marks,splitted)
    isolated=map(URL_Isolate, filtered)
    return isolated

def Move_From_N_To_C(size):
    """ Move_From_N_To_C(size) -> None

        Moves size items from the Queue NLevel to the Queue CLevel
    """
    global found
    for i in xrange(size):
        if found: #The Threads are working in this time, thus the destination may be found. If it is - there is no need to continue.
            break
        CLevel.put(NLevel.get())
        print i, #For the record.

def Print_Path(Destination, Listed_Articles):
    """ Print_Path(Destination, Listed_Articles) --> None

    prints the path that was taken from the first page to the destination page,
    using the information in the "Listed Articles" dictionary
    """
    path=[]
    temp=Destination
    while temp!="Origin": #Writing the path, starting from the ending and going backwards
        path.insert(0,temp)
        temp=Listed_Articles[temp]
    print "The path is:\n"
    for link in path: 
        print link[29:] #[:29] removes the "http://en.wikipedia.org/wiki/ part of the url, leaving only the actual name of the
        if not link==Destination:
            print "|\nV "


#=========================

#=========================
NUM=300

def doWork():
    global CLevel, NLevel, Listed_Articles, Destination, found #Variables that need to be global.
    while not found:
        #print "E",
        Temp_Origin=CLevel.get() #get URL from work Queue
        print "G", #For the record
        if found: #If the detanition was found, just do task_done() so that the lock [of the join()] will be unlocked.
            CLevel.task_done()

        else:
            ##---------Source Code Fetching:---------##
            try:
                request=urllib2.Request(Temp_Origin) #Request file creation
                response=urllib2.urlopen(request) #Response file creation
            except urllib2.HTTPError or ValueError or httplib.BadStatusLine: #exception management - if there's a problem with the URL the Thread will simply do task_done to him and will gom to the next URL
                CLevel.task_done()
                continue
            else:
                source_code=response.read()
                ##---------URL Isolation---------##
                URLs=Get_URLs(source_code)
                ##---------URL Scanning---------##
                for link in URLs: #Scanning all the links in the current page
                    if link.startswith("/wiki/"):        #Some links in the source page start with /wiki/ but they are legitimate wikipedia articles
                        link="http://en.wikipedia.org"+link #So we add the "classic" article "Prefix" so the program will recognize it.
                    if Is_Wiki_Article(link) and not (link in Listed_Articles.keys()) and not link=="http://en.wikipedia.org/wiki/Main_Page":
                        Listed_Articles[link]=Temp_Origin #Entering the verified link to the dictionary as a key with it's "parent page" as it's value
                        if link==Destination:
                            found=True
                            break
                        else:
                            NLevel.put(link) #if the current link isn't the destination it's added to the Queue of links to check (the Queue of the next level)
                            

                CLevel.task_done()

@timecall
def Main():
    global CLevel, NLevel, Listed_Articles, Destination, found, steps #Variables that need to be global.

    #---------Origin Input:---------#
    validated=False
    while not validated:
        Origin=raw_input("\nOrigin page: ")
        validated = Validate(Origin)
        
    #---------Destination Input:---------#
    validated=False
    while not validated:
        Destination=raw_input("Destination page: ")
        validated = Validate(Destination)
        
    #---------Travel Length Input:---------#
    while True:
        try:
            Max_Steps=int(raw_input("Maximum travel length (a non-negative number): "))
            if Max_Steps<0: #since we want a non-negative number, a value error is being raised if the input is negative.
                raise ValueError
        except ValueError:
            print("An error accured. Please try again.")
        else:
            break

    #---------Running Preparations:---------#
    Start_Time=time.asctime(time.localtime())
    print "started at:",Start_Time #Just for the record
    steps=0

    CLevel = Queue.Queue() #Current level Queue - the work Queue
    NLevel = Queue.Queue() #The next level's Queue of links - see useg.

    Listed_Articles={Origin:"Origin"} #This dictionary saves each link of every visited article as a key, with it's value representing the first
                                      #page that linked to it (in other words - from which page did it get to it)
    print "==="
    #---------Origin Is Destination?:---------#
    if Origin==Destination: #If the origin and the destinations are the same page, there's no point checking for a path...
        found=True
    else:
        found=False
            
    #---------Creating Threads:---------#
    for i in xrange(NUM):
        t = threading.Thread(target=doWork)
        t.deamon = True
        t.start()
            
    #---------Main Function:---------#
    CLevel.put(Origin) #First Thread takes it and start working
    while not found and steps<Max_Steps:
        CLevel.join() #Wait for end of prossing of the links to be ended
        if not NLevel: #If NLevel is empty, we are out of links to check.
            break
        steps+=1
        Print_Info()
        print "B:", NLevel.qsize() #For the record
        Move_From_N_To_C(NLevel.qsize()) #The Threads are waiting for tasks from CLevel [as an object, not a reference],
                                         #thus we need to move them from Nlevel to CLevel; but only as many as there are now
                                         #[because the Threads will add to NLevel during the transmision].
        print "A:", NLevel.qsize() #For the record
            
    #---------Post-Main Run:---------#
    if not found: #if the destination wasen't reached
        print ("There is no path shorter or equal in length to the maximum travel length which was inputted from the Origin to the Destination that were chosen.\n Sorry :(")
    else: #if the destination was reached
        Print_Path(Destination, Listed_Articles)
            
    print "\nStarted at:\n        ",Start_Time,\
          "\nended at:\n        ",time.asctime(time.localtime()),\
          "\nand went through",len(Listed_Articles),"articles" #Just for the record

    #---------Again?:---------# ******This can't work due to problem with threads******

Main()
