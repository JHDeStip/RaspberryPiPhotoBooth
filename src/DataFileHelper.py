import os

class DataFileHelper(object):
    _dataFilePath = None

    def __init__(self, dataFile):
        self._dataFilePath = os.path.join(os.path.split(os.path.abspath(__file__))[0], dataFile)

    def getLastPhotoNumbers(self):
        file = None
        lastAcceptedPhotoNumber = 0
        lastDiscartedPhotoNumber = 0

        if os.path.isfile(self._dataFilePath):
            try:
                file = open(self._dataFilePath, "r")
                lines = file.readlines()
                lastAcceptedPhotoNumber = int(lines[0])
                lastDiscartedPhotoNumber = int(lines[1])
            finally:
                if file:
                    file.close()

        return lastAcceptedPhotoNumber, lastDiscartedPhotoNumber

    def saveLastPhotoNumbers(self, lastPhotoNumbers):
        file = None
        try:
            file = open(self._dataFilePath, "w")
            file.write(str(lastPhotoNumbers[0]) + "\n" + str(lastPhotoNumbers[1]))
            file.close()
            return True
        finally:
            if file:
                file.close()
        
        return False