import Constants
import datetime
import os
from PIL import Image

class ImageSaveHelper(object):
    _JPEG_EXTENSION = ".jpg"

    _dataFileHelper = None
    _jpegQuality = 0
    _acceptedFolder = None
    _discardedFolder = None
    _mirrorSavedPhoto = False

    _lastAcceptedPhotoNumber = 0
    _lastDiscartedPhotoNumber = 0

    def __init__(self, dataFileHelper, jpegQuality, acceptedFolder, discardedFolder, mirrorSavedPhoto):
        self._dataFileHelper = dataFileHelper
        self._jpegQuality = jpegQuality
        self._acceptedFolder = acceptedFolder
        self._discardedFolder = discardedFolder
        self._mirrorSavedPhoto = mirrorSavedPhoto
        self._lastAcceptedPhotoNumber, self._lastDiscartedPhotoNumber = self._dataFileHelper.getLastPhotoNumbers()

    def saveImage(self, image, accepted):
        try:
            if self._mirrorSavedPhoto:
                image.transpose(Image.FLIP_LEFT_RIGHT)

            currentTime = datetime.datetime.now()
            if currentTime > datetime.datetime.strptime(Constants.TRESHOLD_TIME, Constants.TIME_FORMAT):
                timestring = currentTime.strftime("_" + Constants.TIME_FORMAT)
            else:
                timestring = ""

            filePath = None

            if accepted:
                self._lastAcceptedPhotoNumber += 1
                filePath = os.path.join(self._acceptedFolder, str(self._lastAcceptedPhotoNumber) + timestring + self._JPEG_EXTENSION)
            else:
                self._lastDiscartedPhotoNumber += 1
                filePath = os.path.join(self._discardedFolder, str(self._lastDiscartedPhotoNumber) + timestring + self._JPEG_EXTENSION)

            if not self._dataFileHelper.saveLastPhotoNumbers((self._lastAcceptedPhotoNumber, self._lastDiscartedPhotoNumber)):
                return False

            image.save(filePath, "JPEG", quality=self._jpegQuality)

            return True
        except:
            return False