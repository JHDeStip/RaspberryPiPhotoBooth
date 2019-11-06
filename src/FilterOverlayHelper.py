from PIL import Image
import os

class FilterOverlayHelper(object):
    _overlayResolutionHelper = None
    _photoResolution = None
    _filterOverlayFilePath = None
    photoFilterOverlay = None
    previewFilterOverlay = None

    def __init__(self, overlayResolutionHelper, photoResolution, filterOverlayFilePath):
        self._overlayResolutionHelper = overlayResolutionHelper
        self._photoResolution = photoResolution
        self._filterOverlayFilePath = filterOverlayFilePath


    def loadFilterOverlay(self):
        self.photoFilterOverlay = self.getFilterOverlay()
        self.previewFilterOverlay = self.getPreviewFilterOverlay(self.photoFilterOverlay)


    def getFilterOverlay(self):
        try:
            if not os.path.exists(self._filterOverlayFilePath):
                return None

            image = Image.open(self._filterOverlayFilePath)
            if not image.size == self._photoResolution:
                print("Error: filter overlay must match the photo resolution ({}X{}).".format(self._photoResolution[0], self._photoResolution[1]))
                return None
            
            return image
        except:
            print("Error: cannot open filter overlay.")


    def getPreviewFilterOverlay(self, photoFilterOverlay):
        if photoFilterOverlay == None:
            return None

        image = photoFilterOverlay.copy()

        return self._overlayResolutionHelper.resizeImageForOverlay(image, False)