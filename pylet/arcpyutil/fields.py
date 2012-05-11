""" This module contains utilities for tabular fields accessed using `arcpy`_, a Python package associated with ArcGIS. 

    .. _arcpy: http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/What_is_ArcPy/000v000000v7000000/
    .. _FieldMappings: http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/FieldMappings/000v0000008q000000/
    .. _arcpy.DeleteField_management: http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//00170000004n000000
    .. _iterable: http://docs.python.org/glossary.html#term-iterable
"""

import os
import arcpy



def getSortedFieldMappings(tablePath, putTheseFirst):
    """ Get an alphabetically sorted arcpy `FieldMappings`_ object for the given table, with the specified fields up 
    front.

    **Description:**

        Given a path to a table or feature class, an arcpy `FieldMappings`_ object is returned with fields sorted
        alphabetically.  Fields specified in putTheseFirst list are put at the start in the same order specified.
        
        Example of usage::
        
            fieldMappings = pylet.arcpyutil.fields.getSortedFieldMappings(inTablePath, putTheseFirst)
            arcpy.TableToTable_conversion(inTablePath, outWorkspace, outName, None, fieldMappings)        
        
    **Arguments:**
        
        * *tablePath* - path to a table or feature class with fields you wish to sort  
        * *putTheseFirst* - list of field names to put first; order of fields is matched  
        
        
    **Returns:** 
        
        * arcpy `FieldMappings`_ object 


        
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
    
    # Assemble each fieldMap into FieldMappings object
    for fieldMap in fieldMaps:
        fieldMappings.addFieldMap(fieldMap)

    return fieldMappings


def getFieldNameSizeLimit(outTablePath, fixes=None):
    """ Return the maximum size of output field names based on the output location of the table being created.

    **Description:**
        
        The value returned is based on the output table's type.  The table's type is determined by parsing the full 
        path to the table and first looking at the suffix for the workspace and then for the file.  The values are 
        returned based on these rules:
        
        * 64  -  file and personal geodatabases(folder with .mdb or .gdb extension)
        * 10  -  dBASE tables (file with .dbf or .shp extension)
        * 16  -  INFO tables (default if previous identifiers were not found
        
        The length of *fixes* will be subtracted from this number.  The *fixes* argument can be a single string or
        a list of strings that might be added to a root field name for which you need the length.
        
        SDE databases are not unsupported.
        
    **Arguments:**
        
        * *outTablePath* - Full path to output table
        * *fixes* - A string or list of strings
        
    **Returns:** 
        
        * integer

    """

        
    outTablePath, outTableName = os.path.split(outTablePath)
    
    folderExtension = outTablePath[-3:].lower()
    fileExtension = outTableName[-3:].lower()
    
    if  folderExtension == "gdb" :
        maxFieldNameSize = 64 # ESRI maximum for File Geodatabases
    elif folderExtension == "mdb":
        maxFieldNameSize = 64 # ESRI maximum for Personal Geodatabases
    elif fileExtension == "dbf" or fileExtension == "shp":
        maxFieldNameSize = 10 # maximum for dBASE tables
    else:
        maxFieldNameSize = 16 # maximum for INFO tables
        
    if fixes:
        #fixes is a list
        if isinstance(fixes, list):
            extraLength = sum((len(fix) for fix in fixes ))
        #fixes is a string
        else:
            extraLength = len(fixes)
        
    return maxFieldNameSize - extraLength


def deleteFields(inTable, fieldNames):
    """ In the given input table, delete all fields with the specified names.
    
    **Description:**
        

        The `arcpy.DeleteField_management`_ tool is used to delete each field name from the input table.  The field 
        name is not case sensitive.
        
    **Arguments:**
        
        * *inTable* - Object or string indicating the input table with fields that need to be deleted
        * *fieldNames* - An `iterable`_ containing field names to delete
        
    **Returns:** 
        
        * None
        
    """ 
    for fieldName in fieldNames:
        arcpy.DeleteField_management(inTable, fieldName)
        


def getFieldByName(inTable, fieldName):
    """ In the given table, return the arcpy `Field`_ object with the given name.

    **Description:**
        
        Fields in the input table are searched using arcpy.ListFields.  Names are converted to lowercase for the 
        comparison.
        
    **Arguments:**
        
        * *inTable* - input table or feature class to retrieve field object from
        * *fieldName* - the name of the field
        
    **Returns:** 
        
        * arcpy `Field`_ object 
        
        .. _Field: http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/Field/000v00000071000000/
        
    """    
    
    idField = None
    
    for field in arcpy.ListFields(inTable):
        if str(field.name).lower() == str(fieldName).lower():
            idField = field
            break
        
    return idField