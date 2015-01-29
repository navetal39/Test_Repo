def Starts_With_Quotation_marks(x):
    """ Starts_With_Quotation_marks(string) --> bool

        returns true if x starts with the char '"', else returns false.
    """
    return x.startswith('"')

def URL_Isolate(x):
    """ URL_Isolate(string) --> string

        returnd a substring of x from the first index in which tha char
        '"' appears to the last index in which tha char '"' appears.
    """
    l=x.split('"')
    newX=l[1]
    return newX

def Is_Wiki_Article(URL):
    """ Is_Wiki_Article (string) --> bool

        returns true if x matches the format of an article in the english
        version of wikipedia, else returns false.

    """
    return URL.startswith("http://en.wikipedia.org")
