""" This module contains utilities for raster datasets or objects accessed using `arcpy`_, a Python package associated with ArcGIS. 

    .. _arcpy: http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/What_is_ArcPy/000v000000v7000000/
"""

import arcpy as _arcpy

def getRasterPointFromRowColumn(raster, row, column):
    """ Get an arcpy `Point`_ object from an arcpy `Raster`_ object and zero based row and column indexes.

        **Description:**
        
        The row and column are zero-based and start in the upper left corner.  The arcpy `Point`_ object returned has
        X and Y coordinates representing the cell identified by the specified row and column.
        
        
        **Arguments:**
        
        * *raster* - arcpy `Raster`_ object
        * *row* - integer representing the zero based index of the row
        * *column* - integer representing the zero based index of the column
        
        
        **Returns:** 
        
        * arcpy `Point`_ object 
        
        .. _Point: http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/Point/000v000000mv000000/
        .. _Raster: http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/Raster/000v000000wt000000/

        
    """    

    
    extent = raster.extent    
    upperLeftX = extent.XMin
    upperLeftY = extent.YMax

    xDistanceFromUpperLeft = column * raster.meanCellWidth
    yDistanceFromUpperLeft = row * raster.meanCellHeight
    
    x = upperLeftX + xDistanceFromUpperLeft
    y = upperLeftY - yDistanceFromUpperLeft

    point = _arcpy.Point(x,y)
    
    return point 