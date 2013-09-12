""" This module contains utilities for environment settings accessed using `arcpy`_, a Python package associated with ArcGIS. 

    .. _arcpy: http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/What_is_ArcPy/000v000000v7000000/
    .. _iterable: http://docs.python.org/glossary.html#term-iterable
    .. _env: http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/env/000v00000129000000/
    .. _System Temp: http://docs.python.org/library/tempfile.html#tempfile.gettempdir
    
"""

import tempfile
import arcpy
from arcpy import env


def getWorkspaceForIntermediates(fallBackWorkspace=None):
    """ Get the full path to a workspace for intermediate datasets.
    
    **Description:**
    
        Priorities are searched to return the directory that should be used for intermediate datasets.  The priorities 
        are as follows:
        
        1. `env`_.scratchWorkspace - ArcGIS environment setting
        2. `env`_.workspace - ArcGIS environment setting
        3. `System Temp`_ - Based on system variables and existing folders
        4. *fallBackWorkspace* - The default is None.
         
        It seems that some tools still have issues with spaces in the pathname, so that test will be added.
        
        
    **Arguments:**
        
        * *fallBackWorkspace* - Full path to a workspace fallback if all other priorities are null 
        
        
    **Returns:**
        
        * string - full path to a workspace
    
    """
    
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
    
    # User supplied directory or default None
    if spaceCheck(fallBackWorkspace):
        return fallBackWorkspace
    else:
        msg = """All available temp workspaces are either null or contain spaces, which may cause errors. Please set the 
        ScratchWorkspace geoprocessing environment setting to a directory or file geodatabase whose full path contains no spaces."""
        arcpy.AddMessage(msg)
        

def spaceCheck(path):
    """Returns true if path is not null and does not contain spaces, otherwise returns false"""
    if path and not " " in path:
        return True
    else: 
        return False