import Constants
from picamera import PiResolution
from PIL import Image

class OverlayResolutionHelper(object):
    _SUPPORTED_HDMI_GROUP = "2"
    _HDMI_GROUP_KEY = "hdmi_group"
    _HDMI_MODE_KEY = "hdmi_mode"

    _RESOLUTIONS = {
        "1": (640, 350),
        "2": (640, 400),
        "3": (720, 400),
        "4": (640, 480),
        "5": (640, 480),
        "6": (640, 480),
        "7": (640, 480),
        "8": (800, 600),
        "9": (800, 600),
        "10": (800, 600),
        "11": (800, 600),
        "12": (800, 600),
        "13": (800, 600),
        "14": (848, 480),
        "15": (1024, 768),
        "16": (1024, 768),
        "17": (1024, 768),
        "18": (1024, 768),
        "19": (1024, 768),
        "20": (1024, 768),
        "21": (1152, 864),
        "22": (1280, 768),
        "23": (1280, 768),
        "24": (1280, 768),
        "25": (1280, 768),
        "26": (1280, 768),
        "27": (1280, 800),
        "28": (1280, 800),
        "29": (1280, 800),
        "30": (1280, 800),
        "31": (1280, 800),
        "32": (1280, 960),
        "33": (1280, 960),
        "34": (1280, 960),
        "35": (1280, 1024),
        "36": (1280, 1024),
        "37": (1280, 1024),
        "38": (1280, 1024),
        "39": (1360, 768),
        "40": (1360, 768),
        "41": (1400, 1050),
        "42": (1400, 1050),
        "43": (1400, 1050),
        "44": (1400, 1050),
        "45": (1400, 1050),
        "46": (1440, 900),
        "47": (1440, 900),
        "48": (1440, 900),
        "49": (1440, 900),
        "50": (1440, 900),
        "51": (1600, 1200),
        "52": (1600, 1200),
        "53": (1600, 1200),
        "54": (1600, 1200),
        "55": (1600, 1200),
        "56": (1600, 1200),
        "57": (1680, 1050),
        "58": (1680, 1050),
        "59": (1680, 1050),
        "60": (1680, 1050),
        "61": (1680, 1050),
        "62": (1792, 1344),
        "63": (1792, 1344),
        "64": (1792, 1344),
        "65": (1856, 1392),
        "66": (1856, 1392),
        "67": (1856, 1392),
        "68": (1920, 1200),
        "69": (1920, 1200),
        "70": (1920, 1200),
        "71": (1920, 1200),
        "72": (1920, 1200),
        "73": (1920, 1440),
        "74": (1920, 1440),
        "75": (1920, 1440),
        "76": (2560, 1600),
        "77": (2560, 1600),
        "78": (2560, 1600),
        "79": (2560, 1600),
        "80": (2560, 1600),
        "81": (1366, 768),
        "82": (1920, 1080),
        "83": (1600, 900),
        "84": (2048, 1152),
        "85": (1280, 720),
        "86": (1366, 768)   
    }

    overlayResolution = None

    def __init__(self):
        screenResolution = self.readScreenResolution()
        paddedResolution = PiResolution(screenResolution[0], screenResolution[1]).pad(32, 16)
        self.overlayResolution = (paddedResolution[0], paddedResolution[1])


    def readScreenResolution(self):
        try:
            with open(Constants.PI_BOOT_CONFIG_FILE, "r") as config:
                lines = config.readlines()
                
                group = None
                mode = None

                for line in lines:
                    parts = line.rstrip("\n").rstrip("\r").rstrip("\t").rstrip(" ").split("=")
                    parts = line.split("=")
                    if len(parts) == 2:
                        if parts[0].lower() == self._HDMI_GROUP_KEY:
                            group = parts[1]
                        elif parts[0].lower() == self._HDMI_MODE_KEY:
                            mode = parts[1]
                        if group != None and mode != None:
                            break

                if group != self._SUPPORTED_HDMI_GROUP:
                    return Constants.DEFAULT_SCREEN_RESOLUTION

                return self._RESOLUTIONS[mode]
        except:
            return Constants.DEFAULT_SCREEN_RESOLUTION


    def resizeImageForOverlay(self, image, fast = True):
        width = self.overlayResolution[0]
        height = self.overlayResolution[1]
        imageRatio = float(image.size[0]) / image.size[1]
        overlayRatio = float(self.overlayResolution[0]) / self.overlayResolution[1]
        cropLeftRight = 0
        cropTopBottom = 0
        
        if imageRatio > overlayRatio:
            width = int(height * imageRatio)
            if width % 2 != 0:
                width += 1
            cropLeftRight = int((width - self.overlayResolution[0]) / 2)
        elif imageRatio < overlayRatio:
            height = int(width / imageRatio)
            if height % 2 != 0:
                height += 1
            cropTopBottom = int((height - self.overlayResolution[1]) / 2)

        scaleMode = None
        if fast:
            algorithm = Image.NEAREST
        else:
            algorithm = Image.HAMMING


        resizedImage = image.resize((width, height), algorithm)
        resizedImage = resizedImage.crop((cropLeftRight, cropTopBottom , width - cropLeftRight, height - cropTopBottom))

        return resizedImage