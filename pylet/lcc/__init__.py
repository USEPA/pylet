""" This module contains utilities specific to Land Cover Classification(LCC) XML files. 

    Each class reflects a different portion of the information stored in the XML file. These LCC XML files should have 
    a .lcc file extension.
    
    To access a file, use :py:class:`LandCoverClassification` as the entry point.  
    
    .. _Node: http://docs.python.org/library/xml.dom.html#node-objects    
    .. _frozenset: http://docs.python.org/library/stdtypes.html#frozenset
    .. _dict: http://docs.python.org/library/stdtypes.html#dict
    
"""


from xml.dom import minidom
import os
import sys
import constants
from glob import glob
from collections import defaultdict
from xml.dom.minidom import NamedNodeMap


class LandCoverMetadata(object):
    """ This class holds all the metadata properties associated with the single LCC metadata-`Node`_.

    **Description:**
        
        This class holds all of the information stored within the <metadata> tag of a LCC XML file.          
        
    **Arguments:**
        
        * *metadataNode* - metadata-`Node`_ loaded from a lcc file
       
    """    
    #: The name of the Land Cover Classification
    name = ""
    #: A description of the Land Cover Classification
    description = ""
    
    def __init__(self, metadataNode=None):
    
        if not metadataNode is None:
            self.loadLccMetadataNode(metadataNode)
            

    def loadLccMetadataNode(self, metadataNode):
        """  This method Loads a LCC metadata-`Node`_ to assign all properties associated with this class.        
        
        **Description:**
            
            If the LCC metadata-`Node`_ was not provided as an argument when this class was instantiated, you can load one
            to assign all properties associated with this class.                        
            
        **Arguments:**
            
            * *metadataNode* - LCC metadata-`Node`_ loaded from a lcc file            
            
        **Returns:** 
            
            * None       
                    
        """
        
        self.name = metadataNode.getElementsByTagName(constants.XmlAttributeName)[0].firstChild.nodeValue
        self.description = metadataNode.getElementsByTagName(constants.XmlAttributeDescription)[0].firstChild.nodeValue
        
    def __repr__(self):
        """String representation when printed"""
        return self.__class__.__name__ + "()"   

class LandCoverClass(object):
    """ This class holds all of the properties associated with a LCC class-`Node`_.

    **Description:**
        
        This class holds all of the information stored in a <class> tag within a LCC XML file.  Values may be 
        duplicated in child classes, but only unique valueIds are reported.        
        
    **Arguments:**
        
        * *classNode* - LCC class-`Node`_ loaded from a lcc file
        * *parentLccObj* - The parent :py:class:`LandCoverClassification` object


    """
    #: The unique identifier for the class
    classId = None
    
    #: The name of the class
    name = ''
    
    #: A `dict`_ for all XML attributes associated with the class-`Node`_
    attributes = dict()
    
    #: A `frozenset`_ of all unique identifiers for Values
    uniqueValueIds = frozenset()
    
    #: A `frozenset`_ of all unique identifiers for Classes
    uniqueClassIds = frozenset()
    
    __parentLccObj = None
    
    def __init__(self, classNode=None, parentLccObj=None):
        
        self.__parentLccObj = parentLccObj
        
        if not classNode is None:
            self.loadLccClassNode(classNode)
            
        
    def loadLccClassNode(self, classNode):
        """  This method Loads a LCC class-`Node`_ to assign all properties associated with this class.        
        
        **Description:**
            
            If the LCC class-`Node`_ was not provided as an argument when this class was instantiated, you can load 
            one to assign all properties associated with this class.                        
            
        **Arguments:**
            
            * *classNode* - LCC class-`Node`_ loaded from a lcc file            
            
        **Returns:** 
            
            * None       
        
        """   
 
        # Load specific attributes as object properties
        self.classId = classNode.getAttribute(constants.XmlAttributeId)
        self.name = classNode.getAttribute(constants.XmlAttributeName)   
        if not self.name:
            self.name = ""
            
        # Loop through all child classes to accumulate unique classIds
        tempClassIds = set()
        for landCoverClass in classNode.getElementsByTagName(constants.XmlElementClass):
            classId = str(landCoverClass.getAttribute(constants.XmlAttributeId))
            tempClassIds.add(classId)
        self.uniqueClassIds = frozenset(tempClassIds)
        
        # Loop through all value nodes, in root and in children, to accumulate unique valueIds
        tempValueIds = set()
        parentLccObj = self.__parentLccObj
        includedValueIds = parentLccObj.values.getIncludedValueIds()

        for landCoverValue in classNode.getElementsByTagName(constants.XmlElementValue):
            valueId = int(landCoverValue.getAttribute(constants.XmlAttributeId))
            
            # Values defined as "excluded" are not included here
            if valueId in includedValueIds:
                tempValueIds.add(valueId)
        
        self.uniqueValueIds = frozenset(tempValueIds)
            
        #Load all attributes into dictionary
        self.attributes = {}
        for attributeName, attributeValue in classNode.attributes.items():
            self.attributes[str(attributeName)] = str(attributeValue)
        
        
class LandCoverValue(object): 
    """ This class holds all of the properties associated with a LCC value-`Node`_.

    **Description:**
        
        This class holds all of the information stored in a <value> tag within a LCC XML file.          
        
    **Arguments:**
        
        * *valueNode* - LCC class-`Node`_ loaded from a lcc file

    """

    #: The unique identifier for the value
    valueId = None
    
    #: The name of the value
    name = ''
    
    #: Boolean for whether value is excluded, ie. water
    excluded = None
    
    #: A `dict`_ for all XML attributes associated with the class-`Node`_
    attributes = {}
    
    def __init__(self, valueNode=None):

        self.defaultNodataValue = False
        
        if not valueNode is None:
            self.loadLccValueNode(valueNode)
    
    
    def loadLccValueNode(self, valueNode):
        """  This method Loads a LCC value-`Node`_ to assign all properties associated with this class.
        
        **Description:**
            
            If the LCC value-`Node`_ was not provided as an argument when this class was instantiated, you can load 
            one to assign all properties associated with this class.                        
            
        **Arguments:**
            
            * *valueNode* - LCC value-`Node`_ loaded from a lcc file            
            
        **Returns:** 
            
            * None       
        
        """ 

        self.valueId = int(valueNode.getAttribute(constants.XmlAttributeId))
        self.name = valueNode.getAttribute(constants.XmlAttributeName)
        
        nodata = valueNode.getAttribute(constants.XmlAttributeNodata)
    
        if nodata:
            try:
                self.excluded = bool(nodata)
            except:
                self.excluded = self.defaultNodataValue
        else:
            self.excluded = self.defaultNodataValue
            
        #Load all attributes into dictionary
        self.attributes = {}
        for attributeName, attributeValue in valueNode.attributes.items():
            self.attributes[str(attributeName)] = str(attributeValue)


class LandCoverValues(dict):
    """ This class holds all :py:class:`LandCoverValue` objects.

    **Description:**
        
        This class holds all of the :py:class:`LandCoverValue` objects loaded from the LCC XML file.          
        
    **Arguments:**
        
        * Not applicable

    """ 
    
    __excludedValueIds = None
    __includedValueIds = None
    
    def getExcludedValueIds(self):
        """  Get a `frozenset`_ containing all valueIds to be excluded       
        
        **Description:**
            
            Excluded valueIds are the raster values which a user has assigned to NoData.                       
            
        **Arguments:**
            
            * Not applicable
                        
        **Returns:** 
            
            * `frozenset`_       
        
        """

        
        if self.__excludedValueIds is None:
            
            self.__updateValueIds()

        return self.__excludedValueIds


    def getIncludedValueIds(self):
        """  Get a `frozenset`_ containing all valueIds which are not marked excluded.
        
        **Description:**
            
            Included valueIds are the raster values which a user has not assigned to NoData.  
            
        **Arguments:**
            
            * Not applicable
            
        **Returns:** 
            
            * `frozenset`_       
            
        """
        
        if self.__includedValueIds is None:
            
            self.__updateValueIds()

        
        return self.__includedValueIds
    
    
    def __updateValueIds(self):
        """ Updates internal frozen sets with included/excluded valueIds 
        
        **Description:**
            
            This is a private method to update the stored frozensets which are returned by separate methods.
            
        **Arguments:**
            
            * Not applicable
            
        **Returns:**
            
            * None
        
        """

        excludedValueIds = []
        includedValueIds = []
        
        # Loop through all LCObjects in this container
        for valueId, landCoverValueObj in self.iteritems():

            #Excluded values
            if landCoverValueObj.excluded:
                excludedValueIds.append(valueId)
            
            #Included values
            else:
                includedValueIds.append(valueId)

        self.__excludedValueIds = frozenset(excludedValueIds)
        self.__includedValueIds = frozenset(includedValueIds)        
        
        
    def __repr__(self):
        """String representation when printed"""
        return self.__class__.__name__ + "()"   
        
        
class LandCoverClasses(dict):
    """ This class holds all :py:class:`LandCoverClass` objects.

    **Description:**
        
        This class holds all of the :py:class:`LandCoverClass` objects loaded from the LCC XML file.          
        
    **Arguments:**
        
        * Not applicable

    """  

    # Private frozenset for all unique values
    __uniqueValues = None

    def getUniqueValueIds(self):
        """  Get a `frozenset`_ containing all unique valueIds defined in all classes. 
        
        **Description:**
            
            The valueIds defined as excluded in the values section are not included.                    
            
        **Arguments:**
            
            * Not applicable
                        
        **Returns:** 
            
            * `frozenset`_       
        
        """
        
        if self.__uniqueValues is None:
            
            # Assemble all values found in all classes, repeats are allowed
            tempValues = []
            for _classId, landCoverClassObj in self.iteritems():
                tempValues.extend(landCoverClassObj.uniqueValueIds)

            # repeats purged on conversion to frozenset
            self.__uniqueValues = frozenset(tempValues)
            
        return self.__uniqueValues
    

    def __repr__(self):
        """String representation when printed"""
        return self.__class__.__name__ + "()"   
      
      
class LandCoverClassification(object):
    """ This class holds all the details about a Land Cover Classification(LCC).

    **Description:**
        
        This class holds :py:class:`LandCoverClasses`, :py:class:`LandCoverValues` and :py:class:`LandCoverMetadata`
        objects and has helpful methods for extracting information from them.     
        
    **Arguments:**
        
        * *lccFilePath* - File path to LCC XML file (.lcc file extension)
        * *excludeEmptyClasses* - ignore a class which does not have a value as a descendant(child, child of child, 
        etc.)

    """ 
    #: A :py:class:`LandCoverClasses` object holding :py:class:`LandCoverClass` objects
    classes = LandCoverClasses()
    
    #: A :py:class:`LandCoverValues` object holding :py:class:`LandCoverValue` objects
    values = LandCoverValues()
    
    #: A :py:class:`LandCoverMetadata` object
    metadata = LandCoverMetadata()
    
    __uniqueValueIds = None
    __uniqueValueIdsWithExcludes = None
    
    def __init__(self, lccFilePath=None, excludeEmptyClasses=True):

        if not lccFilePath is None:
            self.loadFromFilePath(lccFilePath, excludeEmptyClasses)


    def loadFromFilePath(self, lccFilePath, excludeEmptyClasses=True):
        """  This method loads a a Land Cover Classification (.lcc) file.
        
        **Description:**
            
            If the file path to a LCC file was not provided as an argument when this class was instantiated, you can 
            load one to assign all properties associated with this class.                        
            
        **Arguments:**
            
            * *lccFilePath* - File path to LCC XML file (.lcc file extension)         
            * *excludeEmptyClasses* - ignore a class which does not have a value as a descendant(child, child of child, 
            etc.)
            
        **Returns:** 
            
            * None       
                    
        """
        
        # Flush cashed objects, dependent of previous file
        self.__uniqueValueIds = None
        self.__uniqueValueIdsWithExcludes = None
        
        self.lccFilePath = lccFilePath
        lccDocument = minidom.parse(lccFilePath)
        
        # Load Values
        valuesNode = lccDocument.getElementsByTagName(constants.XmlElementValues)[0]
        valueNodes = valuesNode.getElementsByTagName(constants.XmlElementValue)
        tempValues = LandCoverValues()
        for valueNode in valueNodes:
            valueId = int(valueNode.getAttribute(constants.XmlAttributeId))
            landCoverValue = LandCoverValue(valueNode)
            tempValues[valueId] = landCoverValue
        self.values = tempValues        
        
        # Load Classes
        classNodes = lccDocument.getElementsByTagName(constants.XmlElementClass)
        tempClasses = LandCoverClasses() 
        for classNode in classNodes:
            
            # if no value elements as descendents(child, child of child, etc.), the class is skipped
            if excludeEmptyClasses and not classNode.getElementsByTagName(constants.XmlElementValue):
                continue

            classId = classNode.getAttribute(constants.XmlAttributeId)
            tempClasses[classId] = LandCoverClass(classNode, self) # passing this lccObj as parent
        self.classes = tempClasses
        
        # Load Metadata
        metadataNode = lccDocument.getElementsByTagName(constants.XmlElementMetadata)[0]
        self.metadata = LandCoverMetadata(metadataNode)        


    
    def getUniqueValueIds(self):
        """  Get a `frozenset`_ containing all unique valueIds in the Land Cover Classification.
        
        **Description:**
            
            The valueIds will be from both the values and classes, which are not defined excluded.                    
            
        **Arguments:**
            
            * Not applicable
                        
        **Returns:** 
            
            * `frozenset`_       
        
        """
        
        if self.__uniqueValueIds is None:
            
            valueIdsInClasses = self.values.getIncludedValueIds()
            valueIdsInValues = self.classes.getUniqueValueIds()
            
            valueIds = list(valueIdsInClasses) + list(valueIdsInValues)
            
            self.__uniqueValueIds = frozenset(valueIds)
            
        return self.__uniqueValueIds


    def getUniqueValueIdsWithExcludes(self):
        """  Get a `frozenset`_ of all unique values in the lcc file with excluded values included.
        
        **Description:**
            
            The valueIds will be from both the values and classes and they will include those defined as excluded.             
            
        **Arguments:**
            
            * Not applicable
                        
        **Returns:** 
            
            * `frozenset`_       
        
        """        


        if self.__uniqueValueIdsWithExcludes is None:
            
            includedValueIds = list(self.getUniqueValueIds())
            excludedValueIds = list(self.values.getExcludedValueIds())
            
            self.__uniqueValueIdsWithExcludes = frozenset(includedValueIds + excludedValueIds)
        
        return self.__uniqueValueIdsWithExcludes
    

    
    