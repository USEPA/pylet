''' arcpy helper utilities specific to parameters dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd dddddddddddddddddddddddddddddddddddddddddddddddddd

    dkdkdkdkd 
'''

import arcpy

PARAMETER_ENCLOSURE = "'"



def getParametersAsText():
    """ Returns list of all arcpy parameters as text
    
    """
    
    count = 0
    textParameters = []
    
    while True:
        try:
            textParameters.append(arcpy.GetParameterAsText(count))
        except: 
            break
    
        
        count += 1
    
    return textParameters   


def splitItemsAndStripDescriptions(delimitedString, descriptionDelim, parameterDelim=";"):
    """ Splits string with delimited item+description to list of items.
    
        The expected input is a string with nested delimiters, with the following format: 
        'item<descriptionDelim>description<parameterDelim>item<descriptionDelim>description'
        e.g., 'for  [pfor] Forest;wetl  [pwetl]  wetland' --> ['for','wetl']
        
        delimitedString:  the full delimited string
        descriptionDelim: The delimeter for item descriptions.  Descriptions are stripped off
        parmeterDelim: The delimiter for parameters.  The default is a semi-colon.
        
    """
    
    delimitedString = delimitedString.replace(PARAMETER_ENCLOSURE,"")
    
    itemsWithDescription = delimitedString.split(parameterDelim)
    
    itemsWithoutDescription = [itemWithDescription.split(descriptionDelim)[0] for itemWithDescription in itemsWithDescription]
    
    return itemsWithoutDescription