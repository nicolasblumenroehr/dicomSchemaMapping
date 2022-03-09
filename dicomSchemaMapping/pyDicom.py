from matplotlib.font_manager import json_dump
import pydicom
import re
from pyDicomImage import pyDicomImage
import logging
#The class, which contains all attributes from the dicom metadata. Those metadata attributes are entangled from the dicom branching with the dataset and sequence function and instantiated as attributes of the class
class pyDicom:
    
    def __init__(self, dicomFile, studyName, seriesName, pyDicomCustomFunction):
        try:
            self.dicomFile=pydicom.dcmread(dicomFile)
        except Exception as e:
            logging.warning("Error for file: %s %s", dicomFile, e)
            self.dicomFile=pydicom.dcmread(dicomFile, force=True)
        
        self.studyName=studyName
        self.seriesName=seriesName
        self.mainDict={}
        self.subDict=self.dataset(self.dicomFile)
        self.__dict__.update(self.mainDict)
        pyDicom.pyDicomCustomFunction=pyDicomCustomFunction  #This function contains the attributes required for the schema, 
        # which are not covered by the dicom internal metadata attributes and provides the logic for multiple branched attributes.
        #The attributes can either be defined within the function
        #The concept works on the principle of class objects and lists, equivalent to json schemas concept of objects and arrays
        #For each array in the json schema, which contains at least one object, there is an additional list attribute in this function, 
        # which is instantiated in the main pyDicom class. This list contains class objects, 
        # which in turn contain the attributes equivalents for the correspondong object properties in the schema, e.g. attribute perImage
        #These class objects can also contain additional lists with class objects, depending on the depth of the schema
        #For the attributes in the schema, which do not contain objects, but primitive data types,
        # the list attributes in this function just need to contain the proper values for those data types, e.g. attribute locationOfLabel
        #self.studyName=studyName
        #self.studyLocation=studyLocation

    def dataset(self, dataset):
        subDict={}
        subList=[]
        for i in dataset:
            if isinstance(i, pydicom.Dataset):
                subList.append(self.dataset(i))
            elif isinstance(i.value, pydicom.Sequence):
                name=i.name.split()
                if len(name)==1:
                    name=name[0].lower()
                else:
                    subname=""
                    for j in name[1:]:
                        subname+=j.capitalize()

                    name=name[0].lower() + subname

                name=re.sub('[^A-Za-z0-9]+', '', name)
                subDict[name]=self.sequence(i.value)
            else:
                name=i.name.split()
                if len(name)==1:
                    name=name[0].lower()
                else:
                    subname=""
                    for j in name[1:]:
                        subname+=j.capitalize()

                    name=name[0].lower() + subname

                name=re.sub('[^A-Za-z0-9]+', '', name)
               
                subDict[name]=i.value
                self.mainDict[name]=i.value

        if len(subList)>0:
            return subList
        else:
            return subDict

    def sequence(self, sequence):
        subDict={}
        subList=[]
        for i in sequence:
            if isinstance(i, pydicom.Dataset):
                subList.append(self.dataset(i))
            elif isinstance(i.value, pydicom.Sequence):
                name=i.name.split()
                if len(name)==1:
                    name=name[0].lower()
                else:
                    subname=""
                    for j in name[1:]:
                        subname+=j.capitalize()

                    name=name[0].lower() + subname

                name=re.sub('[^A-Za-z0-9]+', '', name)
                subDict[name]=self.sequence(i.value)
            else:
                name=i.name.split()
                if len(name)==1:
                    name=name[0].lower()
                else:
                    subname=""
                    for j in name[1:]:
                        subname+=j.capitalize()

                    name=name[0].lower() + subname

                name=re.sub('[^A-Za-z0-9]+', '', name)
                subDict[name]=i.value
                self.mainDict[name]=i.value

        if len(subList)>0:
            return subList
        else:
            return subDict