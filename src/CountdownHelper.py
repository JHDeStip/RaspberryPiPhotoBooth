import time
import Config

class CountdownHelper(object):
    _overlayManager = None
    _countdownTime = 0

    def __init__(self, overlayManager, countdownTime):
        self._overlayManager = overlayManager
        self._countdownTime = countdownTime


    def startCountdown(self):
        currentCountdownTime = self._countdownTime
        while (currentCountdownTime > 0):
            self._overlayManager.showCountdownOverlay(currentCountdownTime)
            time.sleep(0.5)
            self._overlayManager.removeAllOverlays()
            currentCountdownTime -= 1
            if (currentCountdownTime <= 0):
                time.sleep(0.3)
                return
            time.sleep(0.5)