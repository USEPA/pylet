""" This module contains utilities for parameters accessed using `arcpy`_, a Python package associated with ArcGIS. 

    .. _arcpy: http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/What_is_ArcPy/000v000000v7000000/
"""

import arcpy

PARAMETER_ENCLOSURE = "'"



def getParametersAsText():
    """ Get a list of all arcpy parameters as text.

        **Description:**
        
        Uses `arcpy.GetParameterAsText`_ to assemble a list of strings representing parameters from the script that is 
        being executed.
        
        
        **Arguments:**
        
        * Not applicable 
        
        
        **Returns:** 
        
        * list of strings
        
        .. _arcpy.GetParameterAsText: http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//000v00000014000000
    
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
    """ Splits a string of delimited item-description pairs to a list of items.

        **Description:**
        
        This function first splits a string of one or more delimited item-description pairs into a list of 
        item-description pairs.  It then proceeds to strip off the descriptions, leaving just a list of the items. 
        These items are also stripped of leading and trailing whitespace.
        
        For example, these inputs::
            
            descriptionDelim = " - "
            delimitedString = 'item1  -  description1;item2  -  description2' 
        
        result in this output::
        
            ['item1','item2']
        
        
        **Arguments:**
        
        * *delimitedString* - the full delimited string
        * *descriptionDelim* - The delimeter for item descriptions.  Descriptions are stripped off
        * *parmeterDelim* - The delimiter for parameters.  The default is a semi-colon.
        
        
        **Returns:** 
        
        * List of strings
        
        
        
    """    

    
    delimitedString = delimitedString.replace(PARAMETER_ENCLOSURE,"")
    
    itemsWithDescription = delimitedString.split(parameterDelim)
    
    itemsWithoutDescription = [itemWithDescription.split(descriptionDelim)[0].strip() for itemWithDescription in itemsWithDescription]
    
    return itemsWithoutDescription
