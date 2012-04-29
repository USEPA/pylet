''' Utilities to assist with Python's datetime module

    .. _date: http://docs.python.org/library/datetime.html#date-objects
    .. _datetime: http://docs.python.org/library/datetime.html

'''

import datetime

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
        
    if DASH in dateString:
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