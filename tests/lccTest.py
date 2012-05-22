#Created on Nov 9, 2011
#Michael A. Jackson, jackson.michael@epa.gov

''' Testing for pylet.lcc subpackage

'''
import os
from glob import glob
import pylet


def main():
    """"""
    container = 'ATtILA2{0}ToolboxSource'.format(os.sep)
    dirName = pylet.lcc.constants.PredefinedFileDirName
    upOne = '..'
    relPath = os.sep.join((upOne, upOne, container, dirName))
    os.chdir(relPath)
    
    filePaths = glob('*.lcc')
    print filePaths
    
    testLccFiles(filePaths)
    
def testLccFiles(filePaths):
    """"""
    
    indent = "  "
    
    for filePath in filePaths:
        lccObj = pylet.lcc.LandCoverClassification(filePath)
    
        print "METADATA"
        print "  name:", lccObj.metadata.name
        print "  description:", lccObj.metadata.description
        print
        
        
        print "ATTRIBUTES"
        for key, value in lccObj.coefficients.iteritems():
            assert isinstance(value, pylet.lcc.LandCoverCoefficient)
            print indent, "key:", key
            print indent, "coefId:", value.coefId
            print indent, "fieldName:", value.fieldName 
            print      
        print
        
        
        print "VALUES"
        for key, value in lccObj.values.items():
            print indent, "key:", key
            print indent, "valueId:", value.valueId
            print indent, "name:", value.name
            print indent, "excluded:", value.excluded
            assert isinstance(value, pylet.lcc.LandCoverValue)
            print indent, "PHOSPHORUS:", value.getCoefficientValueById('PHOSPHORUS')
            print indent, "NITROGEN:", value.getCoefficientValueById('NITROGEN')
            print indent, "IMPERVIOUS:", value.getCoefficientValueById('IMPERVIOUS')
            print
        print 
        
        
        print "CLASSES - NO HIERARCHY"
        for classId, landCoverClass in lccObj.classes.items():
            print indent, "key:", classId
            print indent, "classId:", landCoverClass.classId
            print indent, "name:", landCoverClass.name
            print indent, "uniqueValueIds:", landCoverClass.uniqueValueIds
            print indent, "uniqueClassIds:", landCoverClass.uniqueClassIds
            print
        print
        
        print "CLASSES - HIERARCHY"
        
        def printDescendentClasses(landCoverClass, indentUnit, indentLevel):
            
            for childClass in landCoverClass.childClasses:
                printDescendentClasses(childClass, indentUnit, indentLevel + 1)
                
                print indentUnit*indentLevel, childClass.classId
            
        for topLevelClass in lccObj.classes.topLevelClasses:
            print indent, topLevelClass.classId 
            printDescendentClasses(topLevelClass, indent, 2)
        print
        
        print "UNIQUE VALUES IN CLASSES"
        print indent, lccObj.classes.getUniqueValueIds()
        print

        print "INCLUDED/EXCLUDED VALUES"
        print indent, "included:", lccObj.values.getIncludedValueIds()
        print indent, "excluded:", lccObj.values.getExcludedValueIds()
        print

        print "UNIQUE VALUES IN OBJECT"
        print indent, "Top level unique value IDs without excludes:", lccObj.getUniqueValueIds()
        print indent, "Top level unique value IDs with excludes:", lccObj.getUniqueValueIdsWithExcludes()
        print
        
        print "---------------------------------------------------------------------------------"
        print
        
    
if __name__ == "__main__":
    main()
    
    


