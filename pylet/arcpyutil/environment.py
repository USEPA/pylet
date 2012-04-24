""" This module contains utilities for environment settings accessed using `arcpy`_, a Python package associated with ArcGIS. 

    .. _arcpy: http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/What_is_ArcPy/000v000000v7000000/
    .. _iterable: http://docs.python.org/glossary.html#term-iterable
    .. _env: http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/env/000v00000129000000/
    .. _System Temp: http://docs.python.org/library/tempfile.html#tempfile.gettempdir
    
"""

import tempfile

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
         
        
    **Arguments:**
        
        * *fallBackWorkspace* - Full path to a workspace fallback if all other priorities are null 
        
        
    **Returns:**
        
        * string - full path to a workspace
    
    """
    
    # Scratch workspace from ArcGIS Environments
    scratchWorkspace = env.scratchWorkspace
    if scratchWorkspace:
        return scratchWorkspace
    
    # Current workspace from ArcGIS Environments
    currentWorkspace = env.workspace
    if currentWorkspace:
        return currentWorkspace
    
    # System temp directory
    systemTempWorkspace = tempfile.gettempdir()
    if systemTempWorkspace:
        return systemTempWorkspace
    
    # User supplied directory or default None
    return fallBackWorkspace