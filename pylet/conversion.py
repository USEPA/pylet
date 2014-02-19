''' Utilities for conversions

'''

def dmsToDecimalDegrees(degrees, minutes=0, seconds=0):
    """  Convert degrees, minutes and seconds  to decimal degrees
    
    *Description:*
    
        This function accepts degrees, minutes or seconds as string, integer or float, to convert to decimal degrees 
        based on the following conditions:
        
        * Strings will be converted to floating point.  If the conversion fails, zero is used for that value
        * Any argument can be passed as a floating point.  For example, degrees=170 and minutes=25.231 will work.
        
    *Arguments:*
        
        * *degrees* - Degrees as a string, int or float
        * *minutes* - Minutes as a string, int or float
        * *seconds* - Seconds as a string, int or float
        
    *Returns:*
        
        * float - represents decimal degrees
    
    """

    # If degrees are a string, convert to float
    if isinstance(degrees, str) or isinstance(degrees, unicode):
        try:
            degrees = float(degrees)
        except:
            degrees = 0
    
    # If minutes are a string, convert to float
    if isinstance(minutes, str) or isinstance(minutes, unicode):
        try:
            minutes = float(minutes)
        except:
            minutes = 0
    
    # If seconds are a string, convert to float
    if isinstance(seconds, str) or isinstance(seconds, unicode):
        try:
            seconds = float(seconds)
        except:
            seconds = 0    
    
    return degrees + minutes/60.0 + seconds/3600.0    



def hundredthsOfInchesToMillimeters (hundredthsOfInches, decimalPlaces=2):
    """ Convert hundredths of inches to mm.
    
    **Description:**
        
        The first argument is a string, integer or float representing hundredths of inches.  This value is 
        converted to millimeters by multiplying by 0.254.  The result is then rounded to the number of decimal places 
        specified in the second argument (the default is two decimal places).  A float is always returned.          
        
    **Arguments:**
        
        * *hundredthsOfInches* - A string, integer or float representing hundredths of inches
        * *decimalPlaces* - An integer to specify the number of decimal places to round to
    
    **Returns:**
        * float
        
    """      
    
    mm = float(hundredthsOfInches) * 0.254
    
    return round(mm, decimalPlaces)
    
    
def fahrenheitToCelsius(tempF, decimalPlaces=2):

    """ Convert Fahrenheit to Celsius.
    
    **Description:**
        
        The first argument is a string, integer or float representing degrees Fahrenheit.  This value is converted 
        to temperature in degrees Celsius by subtracting 32.0 and then dividing by 1.8. The result is then rounded to 
        the number of decimal places specified in the second argument (the default is two decimal places).  A float is 
        always returned.          
        
    **Arguments:**
        
        * *tempF* - A string, integer or float representing degrees Fahrenheit
        * *decimalPlaces* - An integer to specify the number of decimal places to round to
    
    **Returns:**
        * float
        
    """     
    
    tempC = (float(tempF) - 32.0) / 1.8
    
    return round(tempC, decimalPlaces)


def mphToKph(mph, decimalPlaces=2):
    """ Convert miles per hour to kilometers per hour.
    
    **Description:**
        
        The first argument is a string, integer or float representing miles per hour.  This value is converted to 
        kilometers per hour by multiplying by 0.1609344.  The result is then rounded to the number of decimal places 
        specified in the second argument (the default is two decimal places).  A float is always returned.     
        
    **Arguments:**
        
        * *mph* - A string, integer or float representing miles per hour
        * *decimalPlaces* - An integer to specify the number of decimal places to round to
    
    **Returns:**
        * float
        
    """      
    
    kph = float(mph) * 0.1609344
    
    return round(kph, decimalPlaces)


