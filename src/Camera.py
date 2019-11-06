import picamera
import picamera.array
from PIL import Image
import Constants

class Camera(object):
    _camera = None
    _previewStarted = False
    _previewDimensions = None
    _overlays = []
    _filterOverlayImage = None
    _filterOverlay = None

    def __init__(self, overlayResolutionHelper, imageFlip, photoResolution):
        self._previewDimensions = overlayResolutionHelper.overlayResolution
        self._camera = picamera.PiCamera()
        self._camera.resolution = photoResolution
        self._camera.hflip = imageFlip[0]
        self._camera.vflip = imageFlip[1]


    def dispose(self):
        if self._camera != None:
            self._camera.close()
        

    def start(self):
        if not self._camera.preview:
            self._camera.start_preview(resolution=self._previewDimensions)
            self._camera.preview.layer = 4
            self.showFilterOverlay()


    def setBackgroundOverlay(self, overlay):
        self._camera.add_overlay(overlay.tobytes(), size=overlay.size, layer=0)



    def setFilterOverlay(self, overlay):
        self._filterOverlayImage = overlay


    def setOverlay(self, overlay, transparent, layer = 6):
        alpha = 255
        if transparent:
            alpha = 96

        self._overlays.append(self._camera.add_overlay(overlay.tobytes(), size=overlay.size, layer=layer, alpha=alpha))


    def removeAllOverlays(self):
        while self._overlays:
            self._camera.remove_overlay(self._overlays.pop())


    def showPreview(self):
        if self._camera.preview:
            self._camera.preview.alpha = 255
            self.showFilterOverlay()


    def hidePreview(self):
        if self._camera.preview:
            self.hideFilterOverlay()
            self._camera.preview.alpha = 0


    def showFilterOverlay(self):
        if self._filterOverlayImage != None and self._filterOverlay == None:
            self._filterOverlay = self._camera.add_overlay(self._filterOverlayImage.tobytes(), size=self._filterOverlayImage.size, layer=5)


    def hideFilterOverlay(self):
        if self._filterOverlay != None:
            self._camera.remove_overlay(self._filterOverlay)
            self._filterOverlay = None


    def captureStillFullRes(self):
        image = None
        if self._camera.preview:
            stream = picamera.array.PiRGBArray(self._camera)
            self._camera.capture(stream, format="rgb")
            image = Image.fromarray(stream.array, "RGB")
        return image