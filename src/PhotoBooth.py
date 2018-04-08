from enum import Enum

class PhotoBooth(object):
    _camera = None
    _countdownHelper = None
    _capturedImage = None
    _overlayManager = None
    _imageSaveHelper = None
    _buttonListener = None
    _usbHelper = None

    _status = None

    def __init__(self, buttonListener, camera, imageSaveHelper, overlayManager, countdownHelper, usbHelper):
        self._buttonListener = buttonListener
        self._imageSaveHelper = imageSaveHelper
        self._camera = camera
        self._overlayManager = overlayManager
        self._countdownHelper = countdownHelper
        self._usbHelper = usbHelper

        self._status = Status.NOT_STARTED


    def start(self):
        self._camera.start()
        self._status = Status.IDLE
        if self._usbHelper.isMounted():
            self._buttonListener.startListeningForGreenRedButtons()
        else:
            self._overlayManager.showNoUsbOverlay()


    def doCaptureProcedure(self):
        self._countdownHelper.startCountdown()
        self._camera.hidePreview()
        self._capturedImage = self._camera.captureStillFullRes()
        self._overlayManager.showConfirmationImageOverlay(self._capturedImage)


    def redButtonPressed(self):
        self.greenRedButtonPressed(False)


    def greenButtonPressed(self):
        self.greenRedButtonPressed(True)


    def greenRedButtonPressed(self, greenButtonPressed):
        if self._status == Status.IDLE:
            self.doCaptureProcedure()
            self._status = Status.WAITING_FOR_CONFIRMATION
        elif self._status == Status.WAITING_FOR_CONFIRMATION:
            self._camera.showPreview()
            self._overlayManager.removeAllOverlays()
            if not self._imageSaveHelper.saveImage(self._capturedImage, greenButtonPressed):
                self._overlayManager.showErrorOverlay()
                self._buttonListener.stopListeningForGreenRedButtons()
            self._status = Status.IDLE


    def usbRemoved(self):
        self._overlayManager.removeAllOverlays()
        self._overlayManager.showNoUsbOverlay()
        self._status = Status.IDLE
        

    def usbConnected(self):
        self._overlayManager.removeAllOverlays()


class Status(Enum):
    NOT_STARTED, IDLE, WAITING_FOR_CONFIRMATION = range(3)