import Constants
import time
import sys
import os
from ServiceLocator import ServiceLocator

class Bootstrapper(object):
    _buttonListener = None
    _photoBooth = None
    _camera = None
    _usbHelper = None
    _overlayManager = None

    _hadMountError = False;

    def __init__(self):
        try:
            serviceLocator = ServiceLocator();

            self._buttonListener = serviceLocator.buttonListener
            self._photoBooth = serviceLocator.photoBooth
            self._camera = serviceLocator.camera
            self._usbHelper = serviceLocator.usbHelper
            self._overlayManager = serviceLocator.overlayManager

            self._overlayManager.initialize()

            self._buttonListener.setGreenRedButtonCallback(self._photoBooth)
            self._buttonListener.setServiceButtonCallback(self)

            self._usbHelper.mount()

            self._photoBooth.start()
            self._buttonListener.startListeningServiceButton()
            
            while True:
                time.sleep(sys.maxsize)
        finally:
            if self._buttonListener != None:
                self._buttonListener.dispose()
            if self._camera != None:
                self._camera.dispose()
            if self._usbHelper != None:
                self._usbHelper.unmount()


    def serviceButtonShortPressed(self):
        os.system(Constants.SHUT_DOWN_COMMAND)


    def serviceButtonLongPressed(self):
        # This feature is disabled until hardware problems with the button are resolved.
        return
        if self._hadMountError:
            return

        self._camera.showPreview()

        if self._usbHelper.isMounted():
            self._overlayManager.showBusyOverlay()
            self._buttonListener.stopListeningForGreenRedButtons()
            if not self._usbHelper.unmount():
                self._overlayManager.showErrorOverlay()
                self._hadMountError = True
            else:
                self._photoBooth.usbRemoved()
        else:
            if not self._usbHelper.mount():
                self._overlayManager.showErrorOverlay()
                self._hadMountError = True
            else:
                self._photoBooth.usbConnected()
                self._buttonListener.startListeningForGreenRedButtons()