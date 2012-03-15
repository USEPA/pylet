import fields

import arcpy as _arcpy

def getParametersAsText():
    """ Returns list of all arcpy parameters as text
    
    """
    
    count = 0
    textParameters = []
    
    while True:
        try:
            textParameters.append(_arcpy.GetParameterAsText(count))
        except: 
            break
    
        
        count += 1
    
    return textParameters   