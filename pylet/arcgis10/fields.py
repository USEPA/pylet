""" arcpy helper functions specific to fields

    
"""

import os
import arcpy

def getSortedFieldMappings(tablePath, putTheseFirst):
    """ Returns the sorted field mappings of the given table

        DESCRIPTION
        -----------
        Given a path to a table or feature class, a fieldmappings object is returned
        with fields sorted.  Fields specified in putTheseFirst list are put at the
        start in the same order specified.
        
        PARAMETERS
        ----------
        tablePath:  Path to a table or feature class with fields you wish to sort
        putTheseFirst: list of field names to put first, order of fields is matched
        
        RETURNS
        -------
        arcpy FieldMappings object
        
        EXAMPLE OF USAGE
        ----------------
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
                    break

    fieldMappings.removeAll()
    
    for fieldMap in fieldMaps:
        fieldMappings.addFieldMap(fieldMap)

    return fieldMappings


def getFieldNameSizeLimit(outTablePath):
    """ Return the maximum size of output field names based on the output table's destination/type.
    
        outTablePath: Full path to output table
    
        Returns:  Integer
            64  -  file and personal geodatabases
            10  -  dBASE tables
            16  -  INFO tables 
    
    """
        
    outTablePath, outTableName = os.path.split(outTablePath)
   
    if outTablePath[-3:].lower() == "gdb":
        maxFieldNameSize = 64 # ESRI maximum for File Geodatabases
    elif outTablePath[-3:].lower() == "mdb":
        maxFieldNameSize = 64 # ESRI maximum for Personal Geodatabases
    elif outTableName[-3:].lower() == "dbf":
        maxFieldNameSize = 10 # maximum for dBASE tables
    else:
        maxFieldNameSize = 16 # maximum for INFO tables
        
    return maxFieldNameSize


def deleteField(inTable, fieldName):
    """ Delete the supplied field if it exists in the inTable. 
    
        inTable:  input inTable to delete field from, either full path or arcpy inTable object
        fieldName:  name of the field to delete
        
    """
    newFieldsList = arcpy.ListFields(inTable)
    for nFld in newFieldsList:
        if nFld.name.lower() == fieldName.lower(): 
            arcpy.DeleteField_management(inTable, nFld.name)
            break
        
    return


def getFieldObjectByName(inTable, fieldName):
    """ Get the arcpy field object with the given name 
    
        inTable: input table or feature class to retrieve field object from
        fieldName:  the name of the field
        
    """
    
    idField = None
    for field in arcpy.ListFields(inTable):
        if field.name == fieldName:
            idField = field
            break
        
    return idField


