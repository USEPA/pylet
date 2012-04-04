'''
    Created on Mar 20, 2012 by Michael A. Jackson, jackson.michael@epa.gov, majgis@gmail.com
    
    Helper functions for rasters using ArcGIS10   
    
'''

import arcpy as _arcpy

def getRasterPointFromRowColumn(raster, row, column):
    """ From raster object and zero based row,column starting at upper left, return point object 
    
        raster:  arcpy raster object
        row:  zero based row index (starting at upper left)
        column:  zero based column index (starting at upper left)
        
        Example:
        
          raster:
            1,2,3,4   
            5,6,7,8
          row: 0
          column: 2
          
          returns: Point object with x,y coordinates for value 3  

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