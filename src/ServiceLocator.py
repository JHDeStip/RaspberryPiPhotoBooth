from ButtonListener import ButtonListener
from Camera import Camera
from CountdownHelper import CountdownHelper
from OverlayManager import OverlayManager
from ImageSaveHelper import ImageSaveHelper
from DataFileHelper import DataFileHelper
from PhotoBooth import PhotoBooth
from UsbHelper import UsbHelper
from OverlayResolutionHelper import OverlayResolutionHelper
import Config
import Constants
import os

class ServiceLocator(object):
    buttonListener = None
    overlayResolutionHelper = None
    camera = None
    countdownHelper = None
    imageSaveHelper = None
    overlayManager = None
    photoBooth = None
    dataFileHelper = None
    usbHelper = None
    

    def __init__(self):
        self.buttonListener = ButtonListener()
        self.overlayResolutionHelper = OverlayResolutionHelper()
        self.camera = Camera(self.overlayResolutionHelper, (Config.CAMERA_FLIP_HORIZONTAL, Config.CAMERA_FLIP_VERTICAL), Config.PHOTO_RESOLUTION)
        self.overlayManager = OverlayManager(self.overlayResolutionHelper, self.camera, Config.COUNTDOWN_TIME)
        self.countdownHelper = CountdownHelper(self.overlayManager, Config.COUNTDOWN_TIME)
        self.dataFileHelper = DataFileHelper(Constants.DATA_FILE)
        self.imageSaveHelper = ImageSaveHelper(self.dataFileHelper, Config.JPEG_QUALITY, os.path.join(Constants.PHOTOS_FOLDER, Config.ACCEPTED_FOLDER), os.path.join(Constants.PHOTOS_FOLDER, Config.DISCARDED_FOLDER), Config.MIRROR_SAVED_PHOTO)
        self.usbHelper = UsbHelper(Constants.PHOTOS_FOLDER, [Config.ACCEPTED_FOLDER, Config.DISCARDED_FOLDER])
        self.photoBooth = PhotoBooth(self.buttonListener, self.camera, self.imageSaveHelper, self.overlayManager, self.countdownHelper, self.usbHelper)