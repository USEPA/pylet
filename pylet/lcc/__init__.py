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
    name = None
    
    #: A description of the Land Cover Classification
    description = None
    
    def __init__(self, metadataNode=None):
    
        if not metadataNode is None:
            self._loadLccMetadataNode(metadataNode)


    def _loadLccMetadataNode(self, metadataNode):
        """  This method Loads a LCC metadata-`Node`_ to assign all properties associated with this class.        
        
        **Description:**
            
            If the LCC metadata-`Node`_ was not provided as an argument when this class was instantiated, you can load one
            to assign all properties associated with this class.
            
            See the class description for additional details
                    
        """
        
        self.name = metadataNode.getElementsByTagName(constants.XmlAttributeName)[0].firstChild.nodeValue
        self.description = metadataNode.getElementsByTagName(constants.XmlAttributeDescription)[0].firstChild.nodeValue
        

class LandCoverClass(object):
    """ This class holds all of the properties associated with a LCC class-`Node`_.

    **Description:**
        
        This class holds all of the information stored in a <class> tag within a LCC XML file.  Values may be 
        duplicated in child classes, but only unique valueIds are reported.        
        
    **Arguments:**
        
        * *classNode* - LCC class-`Node`_ loaded from a lcc file
        * *parentClass* - The parent :py:class:`LandCoverClass` object


    """
    #: The unique identifier for the class
    classId = None
    
    #: The name of the class
    name = None
    
    #: A `frozenset`_ of all unique identifiers for Values of all descendants
    uniqueValueIds = None
    
    #: A `frozenset`_ of all unique identifiers for Classes of all descendants 
    uniqueClassIds = None
    
    #: A `dict`_ for all XML attributes associated with the class-`Node`_
    attributes = None
    
    #: A `LandCoverClass`_ object for the parent of this class
    parentClass = None
    
    #: A `list`_ of child classes
    childClasses = None
    
    #: A `list`_ of valueIds for all child values
    childValueIds = None
    
    __parentLccObj = None
    _excludeEmptyClasses = None
    
    def __init__(self, classNode=None, parentClass=None, excludeEmptyClasses=True):
        
        self.parentClass = parentClass
        self._excludeEmptyClasses = excludeEmptyClasses
        
        if not classNode is None:
            self._loadLccClassNode(classNode)
        else:
            self.attributes = {}
            
        
    def _loadLccClassNode(self, classNode):
        """  This method Loads a LCC class-`Node`_ to assign all properties associated with this class.        
        
        **Description:**
            
            If the LCC class-`Node`_ was not provided as an argument when this class was instantiated, you can load 
            one to assign all properties associated with this class.                        
            
           See the class description for additional details
           
        """   
 
        # Load class attributes as object properties
        self.classId = str(classNode.getAttribute(constants.XmlAttributeId))
        self.name = str(classNode.getAttribute(constants.XmlAttributeName))
            
        # Process child nodes
        uniqueClassIds = set()
        uniqueValueIds = set()
        self.childClasses = []
        self.childValueIds = []
        
        for childNode in classNode.childNodes:
            
            if isinstance(childNode, minidom.Element):
                
                # Process child classes
                if childNode.tagName == constants.XmlElementClass:
                    
                    # Point of recursion...bottom-most classes are processed first.
                    landCoverClass = LandCoverClass(childNode, self, self._excludeEmptyClasses)
                    
                    
                    if landCoverClass.childClasses or landCoverClass.childValueIds:
                        # Assemble child classes
                        self.childClasses.append(landCoverClass)
                        
                        # Add child classId to uniqueClassIds
                        uniqueClassIds.add(landCoverClass.classId)
                        
                        # Add uniqueClassIds of child
                        uniqueClassIds.update(landCoverClass.uniqueClassIds)
                        
                        # Add uniqueValueIds of child
                        uniqueValueIds.update(landCoverClass.uniqueValueIds)
            
                # Process child values
                elif childNode.tagName == constants.XmlElementValue:
                    valueId = int(childNode.getAttribute(constants.XmlAttributeId))
                    self.childValueIds.append(valueId)
                    uniqueValueIds.add(valueId)
                
        # Get unique IDs from child classes
        self.uniqueClassIds = frozenset(uniqueClassIds)
        self.uniqueValueIds = frozenset(uniqueValueIds)
        
        #Load all attributes into dictionary
        self.attributes = {}
        for attributeName, attributeValue in classNode.attributes.items():
            self.attributes[str(attributeName)] = str(attributeValue)
       
        
class LandCoverValue(object): 
    """ This class holds all of the properties associated with an LCC value-`Node`_.

    **Description:**
        
        This class holds all of the information stored in a <value> tag within a LCC XML file.          
        
    **Arguments:**
        
        * *valueNode* - LCC class-`Node`_ loaded from a lcc file

    """

    #: The unique identifier for the value
    valueId = None
    
    #: The name of the value
    name = ''
    
    #: A boolean for whether value is excluded, ie. water
    excluded = None
    
    # coefId as the key and LandCoverCoefficient as the value.
    _coefficients = {}
        
    def __init__(self, valueNode=None):
        
        if not valueNode is None:
            self._loadLccValueNode(valueNode)
        else:
            self.coefficients = {}
    
    def _loadLccValueNode(self, valueNode):
        """  This method Loads a LCC value-`Node`_ to assign all properties associated with this class.
        
        **Description:**
            
            If the LCC value-`Node`_ was not provided as an argument when this class was instantiated, you can load 
            one to assign all properties associated with this class.                        
            
            See the class description for additional details
        
        """ 

        self.valueId = int(valueNode.getAttribute(constants.XmlAttributeId))
        self.name = valueNode.getAttribute(constants.XmlAttributeName)
        
        nodata = valueNode.getAttribute(constants.XmlAttributeNodata)
    
        if nodata:
            try:
                self.excluded = bool(nodata)
            except:
                self.excluded = False
        else:
            self.excluded = False
        
        # Load coefficients
        self._coefficients = {}
        for coefficientNode in valueNode.getElementsByTagName(constants.XmlElementCoefficient):
            lcCoef = LandCoverCoefficient(coefficientNode)
            self._coefficients[lcCoef.coefId] = lcCoef
    
    def getCoefficientValueById(self, coeffId):
        """  Given the unique identifier for a coefficient, this method returns the corresponding coefficient value. 
        
        **Description:**
        
            A LandCoverValue can have multiple coefficients.  This method allows you to look up the actual coefficient
            value as a floating point number based on the coefficient's unique identifier.  If you need additional 
            details about a coefficient, see the :py:class:`LandCoverCoefficients` property associated with 
            :py:class:`LandCoverClassification`.
        
        **Arguments:**
            
            * *coeffId* - Coefficient unique identifier, ie. IMPERVIOUS, NITROGEN, PHOSPHORUS, etc.
        
        **Returns:**
            
            * float
        
        """
        
        try:
            coeffValue = self._coefficients[coeffId].value
        except:
            coeffValue = None
            
        return coeffValue 


class LandCoverValues(dict):
    """ This class holds all :py:class:`LandCoverValue` objects.

    **Description:**
        
        This class holds all of the :py:class:`LandCoverValue` objects loaded from the LCC XML file.          
        
    **Arguments:**
        
        * Not applicable

    """ 
    
    __excludedValueIds = None
    __includedValueIds = None
    
    def __init__(self, valuesNode=None):
        """ Constructor - Object initialization """
    
        if not valuesNode is None:
            self._loadValuesNode(valuesNode)
    
    def _loadValuesNode(self, valuesNode):
        """ Load values from valuesNode """
        
        valueNodes = valuesNode.getElementsByTagName(constants.XmlElementValue)

        for valueNode in valueNodes:
            valueId = int(valueNode.getAttribute(constants.XmlAttributeId))
            landCoverValue = LandCoverValue(valueNode)
            self[valueId] = landCoverValue
        
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
            
            self._updateValueIds()

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
            
            self._updateValueIds()

        
        return self.__includedValueIds
    
    
    def _updateValueIds(self):
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
               
        
class LandCoverClasses(dict):
    """ This class holds all :py:class:`LandCoverClass` objects.

    **Description:**

        This class holds all of the :py:class:`LandCoverClass` objects loaded from the LCC XML file.          

    **Arguments:**

        * Not applicable

    """

    # Private frozenset for all unique values
    _uniqueValues = None
    
    #: Boolean for exclusion of empty classes
    excludeEmptyClasses = None
    
    #: Top level classes which reside in the root of the <classes> node and have no parent
    topLevelClasses = None

    def __init__(self, classesNode=None, excludeEmptyClasses=True):

        self.excludeEmptyClasses = excludeEmptyClasses
        
        if not classesNode is None:
            self._loadClassesNode(classesNode)
        

    def _loadClassesNode(self, classesNode):

        self.topLevelClasses = []

        for childNode in classesNode.childNodes:

            if isinstance(childNode, minidom.Element) and childNode.tagName == constants.XmlElementClass:
                topLevelClass = LandCoverClass(childNode, None, self.excludeEmptyClasses)
                self.topLevelClasses.append(topLevelClass)
                
                # Add topLevelClass and all its descendents to dictionary
                self[topLevelClass.classId] = topLevelClass
                
                for descendentClass in self._getDescendentClasses(topLevelClass):
                    self[descendentClass.classId] = descendentClass
                
                
    def _getDescendentClasses(self, landCoverClass):
        
        descendentClasses = []

        for childClass in landCoverClass.childClasses:
            descendentClasses += self._getDescendentClasses(childClass)
            descendentClasses.append(childClass)       
        
        return descendentClasses

    def getUniqueValueIds(self):
        """  Get a `frozenset`_ containing all unique valueIds defined in all classes.

        **Description:**

            The valueIds defined as excluded in the values section are not included.

        **Arguments:**

            * Not applicable

        **Returns:** 
            
            * `frozenset`_
        
        """
        
        if self._uniqueValues is None:
            
            # Assemble all values found in all classes, repeats are allowed
            tempValues = []
            for landCoverClass in self.itervalues():
                tempValues.extend(landCoverClass.uniqueValueIds)

            # repeats purged on conversion to frozenset
            self._uniqueValues = frozenset(tempValues)
            
        return self._uniqueValues
      
      
class LandCoverCoefficients(dict):
    """ This class holds :py:class:`LandCoverCoefficient` objects.

    **Description:**
        
        This class holds all of the :py:class:`LandCoverCoefficient` objects loaded from the LCC XML file.          
        
    **Arguments:**
        
        * *coefficientsNode* - LCC class-`Node`_ loaded from a lcc file

    """


    # Private frozenset for all unique values
    _uniqueValues = None
    
    def __init__(self, coefficientsNode=None):
    
        if not coefficientsNode is None:
            self._loadLccCoefficientsNode(coefficientsNode)
            
    
    def _loadLccCoefficientsNode(self, coefficientsNode):
        """  This method Loads a LCC coefficients-`Node`_ to assign all properties associated with this class.
        
        **Description:**
            
            If the LCC coefficients-`Node`_ was not provided as an argument when this class was instantiated, 
            you can load one to assign all properties associated with this class.                        
            
        **Arguments:**
            
            * *valueNode* - LCC coefficients-`Node`_ loaded from a lcc file            
            
        **Returns:** 
            
            * None       
        
        """ 
        
        # Load coefficients
        for coefficientNode in coefficientsNode.getElementsByTagName(constants.XmlElementCoefficient):
            lcCoef = LandCoverCoefficient(coefficientNode)
            self[lcCoef.coefId] = lcCoef
            
      
class LandCoverClassification(object):
    """ This class holds all the details about a Land Cover Classification(LCC).

    **Description:**
        
        This class holds :py:class:`LandCoverClasses`, :py:class:`LandCoverValues` and :py:class:`LandCoverMetadata`
        objects and has helpful methods for extracting information from them.     
        
    **Arguments:**
        
        * *lccFilePath* - File path to LCC XML file (.lcc file extension)
        * *excludeEmptyClasses* - ignore a class which does not have a value as a descendant

    """ 
    #: A :py:class:`LandCoverClasses` object holding :py:class:`LandCoverClass` objects
    classes = None
    
    #: A :py:class:`LandCoverValues` object holding :py:class:`LandCoverValue` objects
    values = None
    
    #: A :py:class:`LandCoverMetadata` object
    metadata = None
    
    #: A `dict`_ holding :py:class:`LandCoverCoefficient` objects
    coefficients = None
    
    __uniqueValueIds = None
    __uniqueValueIdsWithExcludes = None
    
    
    def __init__(self, lccFilePath=None, excludeEmptyClasses=True):

        if not lccFilePath is None:
            self._loadFromFilePath(lccFilePath, excludeEmptyClasses)
        else:
            self.classes = LandCoverClasses()
            self.values = LandCoverValues()
            self.metadata = LandCoverMetadata()
            self.coefficients = LandCoverCoefficients()


    def _loadFromFilePath(self, lccFilePath, excludeEmptyClasses=True):
        """  This method loads a a Land Cover Classification (.lcc) file.
        
        **Description:**
            
            If the file path to a LCC file was not provided as an argument when this class was instantiated, you can 
            load one to assign all properties associated with this class.                        
            
            See the class description for additional details     
                    
        """
        
        # Flush cashed objects, dependent of previous file
        self.__uniqueValueIds = None
        self.__uniqueValueIdsWithExcludes = None
        self.lccFilePath = lccFilePath
        
        # Load file into DOM
        lccDocument = minidom.parse(lccFilePath)
        
        # Load Values
        valuesNode = lccDocument.getElementsByTagName(constants.XmlElementValues)[0]
        self.values = LandCoverValues(valuesNode)      
        
        # Load Classes
        classesNode = lccDocument.getElementsByTagName(constants.XmlElementClasses)[0]
        self.classes = LandCoverClasses(classesNode, excludeEmptyClasses) 
        
        
        # Load Metadata
        metadataNode = lccDocument.getElementsByTagName(constants.XmlElementMetadata)[0]
        self.metadata = LandCoverMetadata(metadataNode)   

        # Load Coefficients
        coefficientsNode = lccDocument.getElementsByTagName(constants.XmlElementCoefficients)[0]
        self.coefficients = LandCoverCoefficients(coefficientsNode)
        
        
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
    


class LandCoverCoefficient(object):
    """ This class holds all of the properties associated with a LCC coefficient-`Node`_.

    **Description:**
        
        This class holds all of the information stored in a <coefficient> tag within XML file.  Some properties are
        not available depending on the context.  The *coefId*, *name* and *fieldName* properties are available from the 
        coefficients section.  The *coefId* and *value* are availiable when associated with a value.          
        
    **Arguments:**
        
        * *coefficientNode* - LCC coefficient-`Node`_ loaded from a lcc file

    """
    
    #: The unique identifier for the coefficient
    coefId = ""
    
    #: The name of the coefficient
    name = ""
    
    #: The name of the field use in output tables
    fieldName = ""
    
    #: The actual coefficient value
    value = ""
    
    
    def __init__(self, coefficientNode=None):
        
        if not coefficientNode is None:
            self._loadLccCoefficientNode(coefficientNode)
    
    
    def _loadLccCoefficientNode(self, coefficientNode):
        """  This method Loads a LCC coefficient-`Node`_ to assign all properties associated with this class.
        
        **Description:**
            
            If the LCC coefficient-`Node`_ was not provided as an argument when this class was instantiated, you can load 
            one to assign all properties associated with this class.                        
            
            See the class description for additional details
        
        """ 

        self.coefId = coefficientNode.getAttribute(constants.XmlAttributeId)
        self.name = coefficientNode.getAttribute(constants.XmlAttributeName)
        self.fieldName = coefficientNode.getAttribute(constants.XmlAttributeFieldName)
        
        try:
            self.value = float(coefficientNode.getAttribute(constants.XmlAttributeValue))
        except:
            self.value = 0.0


  




