""" arcpy helper functions specific to fields

    
"""

import os
import arcpy

def getSortedFieldMappings(tablePath, putTheseFirst):
    """ Return sorted field mappings of the given table

        tablePath:  Path to a table
        putTheseFirst: list of field names to put first; order is matched
        
        Example usage:
        
            fieldMappings = arcpyh.getSortedFieldMappings(inTablePath, putTheseFirst)
            arcpy.TableToTable_conversion(inTablePath, outWorkspace, outName, None, fieldMappings)
        
    """
    
    fieldMappings = arcpy.FieldMappings()
    fieldMappings.addTable(tablePath)

    fieldMaps = [fieldMappings.getFieldMap(fieldIndex) for fieldIndex in range(0,fieldMappings.fieldCount)]
    fieldMaps.sort(key=lambda fmap: fmap.getInputFieldName(0).lower())

    if putTheseFirst:
        # Move those matching putTheseFirst to front of list
        for fieldMapsIndex, fieldMap in enumerate(fieldMaps):
            fieldName = fieldMap.getInputFieldName(0).lower()
            if fieldName in putTheseFirst:
                fieldMaps.insert(0, fieldMaps.pop(fieldMapsIndex))
                
        # Make order of those moved to front of list match putTheseFirst
        for putTheseFirstIndex, inFieldName in enumerate(putTheseFirst):
            for fieldMapsIndex, fieldMap in enumerate(fieldMaps):
                fieldName = fieldMap.getInputFieldName(0).lower()
                if inFieldName == fieldName:
                    if putTheseFirstIndex != fieldMapsIndex:
                        fieldMaps.insert(putTheseFirstIndex, fieldMaps.pop(fieldMapsIndex))
                    break;

    fieldMappings.removeAll()
    
    for fieldMap in fieldMaps:
        fieldMappings.addFieldMap(fieldMap)

    return fieldMappings


def GetFieldNameSizeLimit(outTablePath):
    """ Return the maximum size of output field names based on the output table's destination/type.
    
        outTablePath: Full path to output table
    
        Returns:  Integer
            64  -  file and personal geodatabases
            10  -  dBASE tables
            16  -  INFO tables 
    
    """
        
    outTablePath, outTableName = os.path.split(outTablePath)
   
    if outTablePath[-3:].lower() == "gdb":
        maxFNameSize = 64 # ESRI maximum for File Geodatabases
    elif outTablePath[-3:].lower() == "mdb":
        maxFNameSize = 64 # ESRI maximum for Personal Geodatabases
    elif outTableName[-3:].lower() == "dbf":
        maxFNameSize = 10 # maximum for dBASE tables
    else:
        maxFNameSize = 16 # maximum for INFO tables
        
    return maxFNameSize

