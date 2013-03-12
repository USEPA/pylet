""" This module contains utilities for polygon datasets or objects accessed using `arcpy`_, a Python package associated with ArcGIS. 

    .. _arcpy: http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/What_is_ArcPy/000v000000v7000000/
"""

import arcpy

def getIdAreaDict(polyFc, keyField):
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


def findOverlaps(polyFc):
    """ Get the OID values for polygon features that have areas of overlap with other polygons in the same theme.

        **Description:**
        
        Identify polygons that have overlapping areas with other polygons in the same theme and generate a set of their 
        OID field value. Nested polygons (i.e., polygons contained within the boundaries of another polygon) are also
        selected with this routine. 
        
        
        **Arguments:**
        
        * *polyFc* - Polygon Feature Class
        
        
        **Returns:** 
        
        * set - A set of OID field values

        
    """ 
    
    overlapSet = set()    
    oidField = arcpy.ListFields(polyFc, '', 'OID')[0]
    
    for row in arcpy.SearchCursor(polyFc, '', '', 'Shape; %s' % oidField.name):
        for row2 in arcpy.SearchCursor(polyFc, '', '', 'Shape; %s' % oidField.name):
            # check to see if the polygon overlaps the second shape, or if the second shape is nested within
            if row2.Shape.overlaps(row.Shape) or row2.Shape.contains(row.Shape) and not row2.Shape.equals(row.Shape):
                overlapSet.add(row.getValue(oidField.name))
                overlapSet.add(row2.getValue(oidField.name))
    
    return overlapSet
