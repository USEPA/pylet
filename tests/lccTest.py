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
            print indent, "key:", key, "coefId:", value.coefId, "fieldName:", value.fieldName       
        print
        
        
        print "VALUES"
        for key, value in lccObj.values.items():
            print "  {0:8}{1:8}  {2:40}{3:10}".format(key, value.valueId, value.name, value.excluded)
            assert isinstance(value, pylet.lcc.LandCoverValue)
            for key, value in value.coefficients.iteritems():
                assert isinstance(value, pylet.lcc.LandCoverCoefficient)
                assert isinstance(value.value, float)
                print "              key:", key, "coefId:", value.coefId, "value:", value.value
                
            print
        print 
        
        
        print "ALL CLASSES"
        for classId, landCoverClass in lccObj.classes.items():
            print "  classId:{0:8}classId:{1:8}name:{2:40}{3}{4}".format(classId, landCoverClass.classId, landCoverClass.name, landCoverClass.uniqueValueIds, landCoverClass.uniqueClassIds)
        print
        print "UNIQUE VALUES IN CLASSES"
        print lccObj.classes.getUniqueValueIds()
        print
        print "INCLUDED/EXCLUDED VALUES"
        print "included:", lccObj.values.getIncludedValueIds()
        print "excluded:", lccObj.values.getExcludedValueIds()
        print
        print "UNIQUE VALUES IN OBJECT"
        print "Top level unique value IDs without excludes:", lccObj.getUniqueValueIds()
        print "Top level unique value IDs with excludes:", lccObj.getUniqueValueIdsWithExcludes()

        print
        print "---------------------------------------------------------------------------------"
        print
        
    
if __name__ == "__main__":
    main()
    
    


