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
         * set - A set of OID field values, a dictionary of overlaps, and OID field name
""" 
    
    overlapSet = set()
    overlapDict = {}
    
    oidField = arcpy.ListFields(polyFc, '', 'OID')[0]
    
    for row in arcpy.SearchCursor(polyFc, '', '', 'Shape; %s' % oidField.name):
        idlist = []
        for row2 in arcpy.SearchCursor(polyFc, '', '', 'Shape; %s' % oidField.name):
            # check to see if the polygon overlaps the second shape, or if the second shape is nested within
            if row2.Shape.overlaps(row.Shape) or row2.Shape.contains(row.Shape) and not row2.Shape.equals(row.Shape):
                overlapSet.add(row.getValue(oidField.name))
                overlapSet.add(row2.getValue(oidField.name))

                if row.getValue(oidField.name) not in overlapDict.keys():
                    idlist.append(row2.getValue(oidField.name))
                    overlapDict[row.getValue(oidField.name)] = idlist
                elif row.getValue(oidField.name) in overlapDict.keys():
                    idlist = overlapDict[row.getValue(oidField.name)]
                    idlist.append(row2.getValue(oidField.name))
            elif row2.Shape.within(row.Shape)and not row2.Shape.equals(row.Shape):
                print "Shape Within"
                overlapSet.add(row.getValue(oidField.name))
                overlapSet.add(row2.getValue(oidField.name))

                if row.getValue(oidField.name) not in overlapDict.keys():
                    idlist.append(row2.getValue(oidField.name))
                    overlapDict[row.getValue(oidField.name)] = idlist
                elif row.getValue(oidField.name) in overlapDict.keys():
                    idlist = overlapDict[row.getValue(oidField.name)]
                    idlist.append(row2.getValue(oidField.name))


                
##    print overlapDict

    return overlapSet, oidField.name, overlapDict

def findNonOverlapGroups(overlapDict):
    """ Create a dictionary of unique non overlapping polygons 
        *** Description: ****
        Creates a dictionary of unique list of polygons that do not overlap.
        
        *** Arguments: ***  
        * *Dictionary* - Dictionary of overlapping OIDs
        
        **Returns:** 
        
        * dictionary - A dictionary of OIDs that belong to a group of nonoverlapping polygons 
      
    """ 
    group = 1
    nonoverlapGroupDict = {}
    while len(overlapDict) <> 0:
        alist = []
        #get the first OID in the overlap Dictionary
        k = overlapDict.keys()[0]
        # loop through the dictionary to check which polygons the first oid overlaps
        for z in overlapDict.keys():
            #if OID is not in the overlapDict value for a key then add that key to a list - this means these oids don't overlap the first OID
            if k not in overlapDict[z]:
                alist.append(z)
        #for each of the OID in alist         
        for a in alist:
            #Loop through the overlapDict
            for k in overlapDict.keys():
                #if the OID is in alist
                if k in alist:
                    #then loop through alist
                    for a in alist:
                        #Check to see if any of the OIDs overlap any of the others in the list
                        #if it does then remove it from alist
                        if a in overlapDict[k]:
                            alist.remove(a)


        #Create a new dictionary that groups non overlapping polygons
        nonoverlapGroupDict[group] = alist
        #For each of the OIDs in alist remove them from the overlap Dictionary
        for a in alist:
            del overlapDict[a]
        group = group + 1
    print nonoverlapGroupDict

#    arcpy.AddMessage("Creating non overlapping polygons,new data layers are being created")
    return nonoverlapGroupDict

def createNonOverlapLayers(overlapList, nonoverlapGroupDict, OID, inputLayer, outputLoc, ext):
    """ Create a series of nonoverlapping polygon layers
        *** Description: ****
        A series of "temporary" data layers are created that have
        no overlaps.  The smallest number of polygon layers possible
        is created.
        
        *** Arguments: ***  
        * *overlapList* - List of OIDs with overlapping polygons
        * *nonoverlapGroupDict* - Dictionary of non overlapping polygons
        * *OID * * - Name of the OID field
        
        **Returns:** 
        
        * Temporary Feature Layers * 

        
    """ 
    strlist = []
    flist = []
    fdsc = arcpy.Describe(inputLayer)
    if fdsc.DataType == "ShapeFile":
        outname = fdsc.name.split(".")[0]
    else:
        outname = fdsc.name
    #Create a feature layer of the polygons with no overlaps
    for o in overlapList:
        strlist.append(str(o))
        
    values = ",".join(strlist)
    arcpy.MakeFeatureLayer_management(inputLayer, "No Polygons Overlap",OID + " NOT IN (" + values + ")")
    if int(str(arcpy.GetCount_management("No Polygons Overlap"))) <> 0:
#        arcpy.AddMessage("There are no polygons that do not overlap")
#    else:
        arcpy.FeatureClassToFeatureClass_conversion("No Polygons Overlap", outputLoc, outname + "_0" + ext)
        flist.append(outname + "_0" + ext)

    # Find the group that has the most polygons
    mostpolys = 0
    hiGroup = ""
    for k in nonoverlapGroupDict.keys():
        if len(nonoverlapGroupDict[k]) > mostpolys:
            mostpolys = len(nonoverlapGroupDict[k])
            hiGroup = k
    #Append the group with the most polygs to the No Polygons Overlap layer
    hlist = []
    for h in nonoverlapGroupDict[hiGroup]:
        hlist.append(str(h))
    values = ",".join(hlist)
    arcpy.MakeFeatureLayer_management(inputLayer,  "NoOverlap"+ str(h), OID + " IN (" + values + ")")
    if int(str(arcpy.GetCount_management("No Polygons Overlap"))) == 0:
        arcpy.FeatureClassToFeatureClass_conversion("NoOverlap"+ str(h), outputLoc, outname + "_0" + ext)
        flist.append(outname + "_0" +ext)
    else:
        arcpy.Append_management("NoOverlap" + str(h), outputLoc + "//" + outname + "_0" + ext)

    #remove key with most polygons from nonoverlapGroupDict
    nonoverlapGroupDict.pop(hiGroup, "None")
    
    #Create a feature layer of polygons of each group of non overlapping polygons
    num = 1
    for k in nonoverlapGroupDict.keys():
        olist = []
        for o in nonoverlapGroupDict[k]:
            olist.append(str(o))
        values = ",".join(olist)
        arcpy.MakeFeatureLayer_management(inputLayer, "NoOverlap" + str(k), OID + " IN (" + values + ")")
        arcpy.FeatureClassToFeatureClass_conversion("NoOverlap" + str(k), outputLoc, outname + "_" + str(num) + ext)
        flist.append(outname + "_" +str(num) +ext)
        num = num + 1
    print flist


    try:
        #For each layer in flist add them to ArcMap
        for f in flist:
            mxd = arcpy.mapping.MapDocument("Current")
    
            #check to see if there is a datafame named "Layers" if yes add the layers to that frame otherwise
            #add it to the top dataframe
            framelist = [frm.name for frm in arcpy.mapping.ListDataFrames(mxd)]
            if "Layers" in framelist:
                df = arcpy.mapping.ListDataFrames(mxd, "Layers") [0]
            else:
                df = arcpy.mapping.ListDataFrames(mxd)[0]
            addlayer = arcpy.mapping.Layer(outputLoc + "//"+f)
            arcpy.mapping.AddLayer(df, addlayer, "AUTO_ARRANGE")
        arcpy.AddMessage("Adding non overlapping polygon layer(s) to view")
        arcpy.AddMessage("The overlap files have been saved to " + outputLoc)
    except:
        arcpy.AddMessage("The overlap files have been saved to " + outputLoc)
        
