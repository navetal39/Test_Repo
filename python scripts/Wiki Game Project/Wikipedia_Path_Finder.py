import urllib2, sys, time
#sys.path.append('C:\Python27\Lib\profilehooks-1.7')
#from profilehooks import profile, timecall



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

def Print_Info():
    """ Print_Info() --> None

    prints running information.
    """
    print "currently checking:", Temp_Origin[29:]
    print "Listed",len(Listed_Articles),"articles so far"
    print steps, "steps have been taken so far"
    print ('===')

def Get_URLs (source):
    """ Get_URLs (source) --> tuple

        returns all the URLs found in the source page in a tuple
        """
    splitted=source.split("href=")
    filtered=filter(Starts_With_Quotation_marks,splitted)
    isolated=map(URL_Isolate, filtered)
    return isolated


def Pop_Link ():
    """ Pop_Link() --> (string, bool, int)

        returns, in this order, the next link in the link queue, a boolean value that tells weather the program is out of links to
        check or not, and the ammount of extra steps taken (0 if the new link is on the same level as the previous one and 1 if it's on the next one)
    """
    NewSteps=0
    Temp_Origin=Page_Queue.pop()
    if Temp_Origin=="Bookmark!":                                          
        NewSteps+=1
        Page_Queue.insert (0, "Bookmark!") 
        Temp_Origin=Page_Queue.pop()       
        if Temp_Origin=="Bookmark!":
            print "Out of links to check!" 
            return '', True, NewSteps
        else:                              
            return Temp_Origin, False, NewSteps
    return Temp_Origin, False, NewSteps

#--------------------------------------------------------------------#

Try_Again=True
while Try_Again: #See end of code.
    
    #---------Origin Input:---------#
    validated=False
    while not validated:
        Origin=raw_input("Origin page: ")
        validated = Validate(Origin)

    #---------Destination Input:---------#
    validated=False
    while not validated:
        Destination=raw_input("Destination page: ")
        validated = Validate(Destination)

    #---------Travel Length Input:---------#
    while True:
        try:
            Max_Steps=int(raw_input("Maximum travel length: "))
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

    Page_Queue=["Bookmark!", Origin]  #A queue that holds all the links of all the visited articles, in the order of their registry (like in a
                                      #level based scan on binary tree from last year). "Bookmark!" will be explained later
    Listed_Articles={Origin:"Origin"} #This dictionary saves each link of every visited article as a key, with it's value representing the first
                                      #page that linked to it (in other words - from which page did it gate to it)

    #---------Origin Is Destination?:---------#
    if Origin==Destination: #If the origin and the destinations are the same page, there's no point checking for a path...
        found=True
    else:
        found=False
    broken=False #Broken is used later, and it will be explained when it'll be used
    
    #---------Main Function:---------#
    while not found and steps<Max_Steps:

        out=False #out will turn true if/when the program is out of links to check.
        Temp_Origin,out,NewSteps=Pop_Link() #Temp origin is the article that is currently being checked.
        #---------Bookmarks---------#
        if out:
            break
        steps+=NewSteps
        ##---------Running information:---------##
        Print_Info()
        ##---------Source Code Fetching:---------##
        while True:
            try: 
                request=urllib2.Request(Temp_Origin) #Request file creation
                response=urllib2.urlopen(request) #Response file creation
            except urllib2.HTTPError or ValueError: #exception management - if there's a problem with the URL the program will simply go to the next one
                Temp_Origin,out,NewSteps=Pop_Link()
                Print_Info()
                continue
            else:
                break
        if out: #If the previous loop was broken (if the program ran out of links to check)
            break #Break the current loop as well and end the "Main Function"
        source_code=response.read()
            
        ##---------URL Isolation---------##                                                                     #wanted URL, then some other stuff
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
                    Page_Queue.insert(0,link) #if the current link isn't the destination it's added to the queue of links to check

    #---------Post-Main Run:---------#
    if not found: #if the destination wasen't reached
        print ("There is no path shorter or equal in length to the maximum travel length which was inputted from the Origin to the Destination that were chosen.\n Sorry :(")
    else: #if the destination was reached
        Print_Path(Destination, Listed_Articles)
        
    print "\nStarted at:\n        ",Start_Time,\
          "\nended at:\n        ",time.asctime(time.localtime()),\
          "\nand went through",len(Listed_Articles),"articles" #Just for the record

    #---------Again?:---------#
    success=False        
    print "\nWould you like to try again?"
    answer=str.lower(raw_input ("Yes/No: "))
    while not success:
        if answer=="yes":
            Try_Again=True
            success=True
        elif answer=="no":
            Try_Again = False
            success=True
        else:
            answer=raw_input ("You didn't input what was requested, please try again: ")
