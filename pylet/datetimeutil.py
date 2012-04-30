''' Utilities to assist with Python's datetime module

    .. _date: http://docs.python.org/library/datetime.html#date-objects
    .. _datetime: http://docs.python.org/library/datetime.html
    .. _generator: http://docs.python.org/tutorial/classes.html#generators

'''
from datetime import timedelta
import datetime

def dateRange(startDate, endDate):
    """ A `generator`_ for days as `date`_ object from *startDate* up to and including *endDate*
    
    **Description:**
    
        Treat this function as an iterable that yields `date`_ objects, in one day increments, from the start date up 
        to and including the end date. 
    
    **Arguments:**
    
        * *startDate* - date object for first date in sequence to be generated
        * *endDate* - date object for last date in sequence to be generated 
    
    **Returns:**
        
        * `generator`_ for `date`_ objects in range
    
    
    """
    
    
    for n in range((endDate - startDate).days):
        yield startDate + timedelta(n)

def getDateObjectFromString(dateString, setToFirstOfMonth=False):    
    """ Convert date in different string formats to a `date`_ object.

    **Description:**
    
        The date is determined based on the following rules:
        
        * If the delimiter for the date is /,  the date format is assumed to be MM/DD/YYYY
        * If the delimiter for the date is -, the date format is assumed to be YYYY-MM-DD
        * If neither of these delimiters is found, the date format is assumed to be YYYYMMDD

    **Arguments:**
    
        * *dateString* - string representing date in one of these formats: MM/DD/YYYY, YYYY-MM-DD, YYYYMMDD
        * *setToFirstOfMonth* - boolean, if true, day is set to 1
    
    **Returns:**
        * `datetime`_ `date`_ object
    
    """
    
    FORWARD_SLASH = '/'
    DASH = '-'
    
    if FORWARD_SLASH in dateString:
        month, day, year = dateString.split(FORWARD_SLASH)
            
    elif DASH in dateString:
        year, month, day = dateString.split(DASH)
        
    else:
        year = dateString[0:4]
        month = dateString[4:6]
        day = dateString[6:]
    
    if setToFirstOfMonth:
        day = 1
    
    return getDateObjectFromStrings(month, day, year)    
    
    
    
def getDateObjectFromStrings(month, day, year):
    """ Convert month, day and year in string formats to a `date`_ object.

    **Description:**
    
        The year must be in YYYYY format. Month can be in M or MM format.  Day can be in D or DD format.

    **Arguments:**
    
        * *month* - string or integer representing the month
        * *day* - string or integer representing the day
        * *year* - string or integer in format YYYY representing the year
    
    **Returns:**
        * `datetime`_ `date`_ object
    
    """
    return datetime.date(int(year), int(month), int(day))


def getDateStringFromObject(date, delimiter="-"):
    """ Format date object as a string in format YYYY-MM-DD 
    
    **Description:**
    
        The date object has a year, month and day associated with it.  Each of these is converted to a string
        and joined with the specified delimiter (the default delimiter is a dash).
    
    **Arguments:**
    
        * *date* - `date`_ object
        * *delimiter* - string to separate year, month and day
    
    **Returns:**
        
        * string in format YYYY-MM-DD
    
    """
    
    return "{0}{3}{1:02d}{3}{2:02d}".format(date.year, date.month, date.day, delimiter)





