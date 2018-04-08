import picamera
import picamera.array
from PIL import Image
import Constants

class Camera(object):
    _camera = None
    _previewStarted = False
    _previewDimensions = None
    _overlays = []

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
            self._camera.preview.layer = 3


    def setBackgroundOverlay(self, overlay):
        self._camera.add_overlay(overlay.tobytes(), size=overlay.size, layer=0)


    def setOverlay(self, overlay, transparent, layer = 4):
        alpha = 255
        if transparent:
            alpha = 96

        self._overlays.append(self._camera.add_overlay(overlay.tobytes(), size=overlay.size, layer=layer, alpha=alpha))


    def removeAllOverlays(self):
        while self._overlays:
            self._camera.remove_overlay(self._overlays.pop())


    def hidePreview(self):
        if self._camera.preview:
            self._camera.preview.alpha = 0


    def showPreview(self):
        if self._camera.preview:
            self._camera.preview.alpha = 255


    def captureStillFullRes(self):
        image = None
        if self._camera.preview:
            stream = picamera.array.PiRGBArray(self._camera)
            self._camera.capture(stream, format="rgb")
            image = Image.fromarray(stream.array, "RGB")
        return image