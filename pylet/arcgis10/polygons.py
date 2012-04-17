''' arcpy helper utilities specific to polygons

'''

import arcpy

def getAreasByIdDict(polyFc, keyField):
    """ Calculate polygon areas and import values to dictionary.
        
        DESCRIPTION
        -----------
        Use the keyField ID as the retrieval key for for polygon areas stored in dictionary
    
    
        ARGUMENTS
        ---------
        polyFc: Polygon Feature Class
        keyField: Unique ID field
        
        
        RETURNED
        --------
        Dictionary {ID:area}
    
    """

    SHAPE_FIELD_NAME = "Shape"
    zoneAreaDict = {}
    
    rows = arcpy.SearchCursor(polyFc)
    for row in rows:
        key = row.getValue(keyField)
        area = row.getValue(SHAPE_FIELD_NAME).area
        zoneAreaDict[key] = (area)

    return zoneAreaDict