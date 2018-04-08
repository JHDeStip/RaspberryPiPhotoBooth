import Constants
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import Colors
import UIStrings
import textwrap

class OverlayManager(object):
    _camera = None
    _overlayDimensions = None
    _currentDir = os.path.split(os.path.abspath(__file__))[0]
    _countdownTime = 0

    _noUSBOverlay = None
    _confirmationButtonsOverlay = None
    _busyOverlay = None
    _countDownOverlays = []
    

    def __init__(self, overlayResolutionHelper, camera, countdownTime):
        self._camera = camera
        self._overlayDimensions = overlayResolutionHelper.overlayResolution
        self._countdownTime = countdownTime


    def initialize(self):
        self.generateCountDownOverlays()
        self._confirmationButtonsOverlay = self.getConfirmationButtonsOverlay()
        self._noUsbOverlay = self.getNoUsbOverlay()
        self._busyOverlay = self.getBusyOverlay()
        self._camera.setBackgroundOverlay(Image.new("RGB", self._overlayDimensions, (0, 0, 0)))


    def showCountdownOverlay(self, number):
        if len(self._countDownOverlays) > number - 1:
            self._camera.setOverlay(self._countDownOverlays[number - 1], True)


    def showNoUsbOverlay(self):
        self.removeAllOverlays()
        self._camera.setOverlay(self._noUsbOverlay, True)


    def showBusyOverlay(self):
        self.removeAllOverlays()
        self._camera.setOverlay(self._busyOverlay, True)


    def showErrorOverlay(self):
        self.removeAllOverlays()
        self._camera.setOverlay(self.getErrorOverlay(), True)


    def showConfirmationImageOverlay(self, confirmationImage):
        width = self._overlayDimensions[0]
        height = self._overlayDimensions[1]
        imageRatio = float(confirmationImage.size[0]) / confirmationImage.size[1]
        overlayRatio = float(self._overlayDimensions[0]) / self._overlayDimensions[1]
        cropLeftRight = 0
        cropTopBottom = 0
        
        if imageRatio > overlayRatio:
            width = int(height * imageRatio)
            if width % 2 != 0:
                width += 1
            cropLeftRight = int((width - self._overlayDimensions[0]) / 2)
        elif imageRatio < overlayRatio:
            height = int(width / imageRatio)
            if height % 2 != 0:
                height += 1
            cropTopBottom = int((height - self._overlayDimensions[1]) / 2)

        scaledImage = confirmationImage.resize((width, height), Image.NEAREST)
        scaledImage = scaledImage.crop((cropLeftRight, cropTopBottom , width - cropLeftRight, height - cropTopBottom))
        self._camera.setOverlay(scaledImage, False, 1)
        self._camera.setOverlay(self._confirmationButtonsOverlay, False, 2)


    def removeAllOverlays(self):
        self._camera.removeAllOverlays()


    def generateCountDownOverlays(self):
        for i in range(0, self._countdownTime):
            image = Image.new("RGB", self._overlayDimensions, (255,255,255))
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(os.path.join(self._currentDir, Constants.TEXT_FONT_FILE), round(self._overlayDimensions[1] / 2))

            text = str(i+1)
            textWidth, textHeight = font.getsize(text)

            draw.text(((self._overlayDimensions[0] - textWidth) / 2, (self._overlayDimensions[1] - textHeight) / 2), text, fill=Colors.BLACK, font=font)

            self._countDownOverlays.append(image)


    def getNoUsbOverlay(self):
        image = Image.new("RGB", self._overlayDimensions, (255,255,255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(os.path.join(self._currentDir, Constants.TEXT_FONT_FILE), round(self._overlayDimensions[1] / 4))

        text = UIStrings.NO_USB
        textWidth, textHeight = font.getsize(text)

        draw.text(((self._overlayDimensions[0] - textWidth) / 2, (self._overlayDimensions[1] - textHeight) / 2), text, fill=Colors.BLACK, font=font)

        return image


    def getConfirmationButtonsOverlay(self):
        image = Image.new("RGBA", self._overlayDimensions, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(os.path.join(self._currentDir, Constants.THUMBS_FONT_FILE), int(self._overlayDimensions[1] / 6))

        thumbDown = "B"
        thumbUp = "A"

        thumbDownSize = font.getsize(thumbDown)
        thumbUpSize = font.getsize(thumbUp)
        
        draw.text((self._overlayDimensions[0] / 3 - thumbDownSize[0] / 2, self._overlayDimensions[1] - thumbDownSize[1] - self._overlayDimensions[1] / 20), thumbDown, font=font, fill=Colors.RED)
        draw.text((self._overlayDimensions[0] * (2 / 3) - thumbUpSize[0] / 2, self._overlayDimensions[1] - thumbUpSize[1] - self._overlayDimensions[1] / 20), thumbUp, font=font, fill=Colors.GREEN)

        return image


    def getBusyOverlay(self):
        image = Image.new("RGB", self._overlayDimensions, (255,255,255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(os.path.join(self._currentDir, Constants.TEXT_FONT_FILE), round(self._overlayDimensions[1] / 4))

        text = UIStrings.BUSY
        textWidth, textHeight = font.getsize(text)

        draw.text(((self._overlayDimensions[0] - textWidth) / 2, (self._overlayDimensions[1] - textHeight) / 2), text, fill=Colors.BLACK, font=font)

        return image


    def getErrorOverlay(self):
        image = Image.new("RGB", self._overlayDimensions, (255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(os.path.join(self._currentDir, Constants.TEXT_FONT_FILE), round(self._overlayDimensions[1] / 7))

        wrapped = textwrap.wrap(UIStrings.ERROR, 10)

        linePadding = self._overlayDimensions[1] / 40
        totalHeight = 0
        for line in wrapped:
            totalHeight += font.getsize(line)[1] + linePadding
        totalHeight -= linePadding

        currentHeight = (self._overlayDimensions[1] - totalHeight) / 2
        for line in wrapped:
            lineWidth, lineHeight = font.getsize(line)
            draw.text(((self._overlayDimensions[0] - lineWidth) /2, currentHeight), line, font=font, fill=Colors.BLACK)
            currentHeight += lineHeight + linePadding

        return image