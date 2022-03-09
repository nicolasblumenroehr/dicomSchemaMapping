import os
from pyDicom import pyDicom
import copy

class initialize():
    
    def __init__(self, studyName, studyLocation, pyDicomCustomFunction=None, *args, **kwargs):

        self.allDicomSeries=[]
        for i, j in zip(os.listdir(studyLocation+studyName), range(0, len(args))):
            f = os.path.join(studyLocation+studyName, i)
            seriesName=i
            dicomSeries=pyDicom(f, studyName, seriesName, pyDicomCustomFunction)
            currentKwargs=copy.deepcopy(kwargs)
            try:
                currentKwargs[list(args[j].keys())[0]]=list(args[j].values())[0]
            except:
                pass
            dicomSeries.pyDicomCustomFunction(**currentKwargs)
            self.allDicomSeries.append(dicomSeries)