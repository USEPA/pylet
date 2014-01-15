""" This module contains utilities for environment settings accessed using `arcpy`_, a Python package associated with ArcGIS. 

    .. _arcpy: http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/What_is_ArcPy/000v000000v7000000/
    .. _iterable: http://docs.python.org/glossary.html#term-iterable
    .. _env: http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/env/000v00000129000000/
    .. _System Temp: http://docs.python.org/library/tempfile.html#tempfile.gettempdir
    
"""
import os
import string
import tempfile
import arcpy
from arcpy import env


def getWorkspaceForIntermediates(gdbFilename, fallBackWorkspace=None):
    """ Get the full path to a workspace for intermediate datasets.
    
    **Description:**
        
        Priorities are searched to return the directory that should be used for intermediate datasets.  
        Originally the "fallBackWorkspace" was the lowest priority, but after further discussion, it was determined
        that this was actually the most intuitive and likely least problematic location for the intermediate datasets, 
        so it was given the top priority, despite the name.  The only reason another workspace might be chosen is if
        spaces are found in the pathname, as this apparently still causes issues for some tools.  
        
        The priorities are as follows:
        
        1. *fallBackWorkspace* - This is expected to be set to the output directory for the rest of the data.
        2. `env`_.scratchWorkspace - ArcGIS environment setting
        3. `env`_.workspace - ArcGIS environment setting
        4. `System Temp`_ - Based on system variables and existing folders
        
    **Arguments:**
        
        * *gdbFilename* - Filename for the scratch geodatabase
        * *fallBackWorkspace* - Full path to a workspace fallback if all other priorities are null 
        
        
    **Returns:**
        
        * string - full path to a workspace
    
    """

    # User supplied directory or default None
    if spaceCheck(fallBackWorkspace):
  
        if string.upper(fallBackWorkspace[len(fallBackWorkspace)-4:]) == ".GDB":
            return fallBackWorkspace
        else:
            if not os.path.exists(fallBackWorkspace + "\\" + gdbFilename):
                arcpy.CreateFileGDB_management(fallBackWorkspace, gdbFilename)
            return fallBackWorkspace + "\\" + gdbFilename

    
    # Scratch workspace from ArcGIS Environments
    scratchWorkspace = env.scratchWorkspace
    if spaceCheck(scratchWorkspace):
        return scratchWorkspace
    
    # Current workspace from ArcGIS Environments
    currentWorkspace = env.workspace
    if spaceCheck(currentWorkspace):
        return currentWorkspace

    # System temp directory
    systemTempWorkspace = tempfile.gettempdir()
    if spaceCheck(systemTempWorkspace):
        return systemTempWorkspace
    else:
        msg = """All available temp workspaces are either null or contain spaces, which may cause errors.
         
        Please set the ScratchWorkspace geoprocessing environment setting to a directory or file geodatabase whose full path contains no spaces."""
        arcpy.AddMessage(msg)
      
        

#def spaceCheck(path):
#    """Returns true if path is not null and does not contain spaces, otherwise returns false"""
#    if path and not " " in path:
#        return True
#    else: 
#        return False

def spaceCheck(path):
    if path:
        return True
    else:
        return False
    

def setBufferedExtent(inPoly, inGrid, inCellSize, inWidth=None):
    """ Sets the analysis extent to that of the input theme, but buffered, and aligned to the grid origin.
    
    **Description:**
            
        Certain metrics are sensitive to edge effects. To mitigate for that, the analysis extent should
        be set beyond the extent of the polygon theme. This function takes the extent of the polygon theme
        and buffers it out to a specified distance and aligns that extent to the origin of the input
        input grid. If no specified distance is supplied, the buffer distance is one cell width. This new 
        extent should avoid edge errors with the pff or the edge/core metrics. 
       
      
    **Arguments:**
        
        * *inPoly* - Polygon feature layer
        * *inGrid* - Grid layer to obtain origin
        * *inCellSize* - The cell size used for the analysis (string)
        * *inWidth* - Distance for buffer specified in number of cells (string)
        
        
    **Returns:**
        
        * analysisExtent - buffered extent object
    
    """
    
    import math
    
    polyDesc = arcpy.Describe(inPoly)
    polyExtent = polyDesc.extent
    
    gridDesc = arcpy.Describe(inGrid)
    gridExtent = gridDesc.extent
    
    cellSize = float(inCellSize)
    
    if inWidth:
        expandDist = (int(inWidth) + 1) * cellSize
    else:
        expandDist = cellSize
    
    # take the polygon's extent and shift its lower left point out to align with the grid's cell boundaries
    newLLX = (((polyExtent.XMin - gridExtent.XMin)//cellSize) * cellSize) + gridExtent.XMin
    newLLY = (((polyExtent.YMin - gridExtent.YMin)//cellSize) * cellSize) + gridExtent.YMin

    # take the polygon's extent and shift its upper right point out to align with the grid's cell boundaries 
    newURX = ((math.ceil(((polyExtent.XMax - gridExtent.XMin) / cellSize))) * cellSize) + gridExtent.XMin
    newURY = ((math.ceil(((polyExtent.YMax - gridExtent.YMin) / cellSize))) * cellSize) + gridExtent.YMin
  
    # expand the coordinates of the new extent to help eliminate edge effects
    env.extent = arcpy.Extent((newLLX-expandDist),(newLLY-expandDist),(newURX+expandDist),(newURY+expandDist))


    