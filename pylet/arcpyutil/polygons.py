""" This module contains utilities for polygon datasets or objects accessed using `arcpy`_, a Python package associated with ArcGIS. 

    .. _arcpy: http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/What_is_ArcPy/000v000000v7000000/
"""

import arcpy

def getAreasByIdDict(polyFc, keyField):
    """ Get a dictionary with polygon areas by an id taken from a specified field.

        **Description:**
        
        For the input polygon feature class, a dictionary with the keyField as the retrieval key and polygon area as 
        the associated value.  The polygon area will be in the same units as the datasets projection.  No check is
        made for duplicate keys. The value for the last key encountered will be present in the dictionary.
        
        
        **Arguments:**
        
        * *polyFc* - Polygon Feature Class
        * *keyField* - Unique ID field
        
        
        **Returns:** 
        
        * dict - The item from keyField is the key and shape.area is the value

        
    """    


    SHAPE_FIELD_NAME = "Shape"
    zoneAreaDict = {}
    
    rows = arcpy.SearchCursor(polyFc)
    for row in rows:
        key = row.getValue(keyField)
        area = row.getValue(SHAPE_FIELD_NAME).area
        zoneAreaDict[key] = (area)

    return zoneAreaDict