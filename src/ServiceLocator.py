from ButtonListener import ButtonListener
from Camera import Camera
from CountdownHelper import CountdownHelper
from OverlayManager import OverlayManager
from ImageSaveHelper import ImageSaveHelper
from DataFileHelper import DataFileHelper
from PhotoBooth import PhotoBooth
from UsbHelper import UsbHelper
from OverlayResolutionHelper import OverlayResolutionHelper
from FilterOverlayHelper import FilterOverlayHelper
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
    filterOverlayHelper = None

    def __init__(self):
        self.buttonListener = ButtonListener()
        self.overlayResolutionHelper = OverlayResolutionHelper()
        self.filterOverlayHelper = FilterOverlayHelper(self.overlayResolutionHelper, Config.PHOTO_RESOLUTION, os.path.join(Constants.USB_MOUNT_DIR, Constants.OVERLAY_FILE))
        self.camera = Camera(self.overlayResolutionHelper, (Config.CAMERA_FLIP_HORIZONTAL, Config.CAMERA_FLIP_VERTICAL), Config.PHOTO_RESOLUTION)
        self.overlayManager = OverlayManager(self.camera, self.overlayResolutionHelper, self.filterOverlayHelper, Config.COUNTDOWN_TIME)
        self.countdownHelper = CountdownHelper(self.overlayManager, Config.COUNTDOWN_TIME)
        self.dataFileHelper = DataFileHelper(Constants.DATA_FILE)
        self.imageSaveHelper = ImageSaveHelper(self.dataFileHelper, Config.JPEG_QUALITY, os.path.join(Constants.USB_MOUNT_DIR, Config.ACCEPTED_FOLDER), os.path.join(Constants.USB_MOUNT_DIR, Config.DISCARDED_FOLDER), Config.MIRROR_SAVED_PHOTO)
        self.usbHelper = UsbHelper(Constants.USB_MOUNT_DIR, [Config.ACCEPTED_FOLDER, Config.DISCARDED_FOLDER])
        self.photoBooth = PhotoBooth(self.buttonListener, self.camera, self.imageSaveHelper, self.overlayManager, self.countdownHelper, self.usbHelper, self.filterOverlayHelper)