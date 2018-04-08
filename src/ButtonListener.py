import RPi.GPIO as GPIO
from threading import RLock
import Constants
import datetime
import time

class ButtonListener(object):
    _listeningForServiceButton = False
    _listeningForGreenRedButton = False

    _greenRedButtonCallback = None
    _serviceButtonCallback = None
    
    _serviceButtonPressed = False
    _serviceButtonLastPressedTime = None

    _lock = None

    def __init__(self):
        self._lock = RLock()
        self._serviceButtonLastPressedTime = datetime.datetime.utcnow()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup([Constants.GREEN_BUTTON_PIN], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup([Constants.RED_BUTTON_PIN], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup([Constants.SERVICE_BUTTON_PIN], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    def dispose(self):
        with self._lock:
            GPIO.cleanup()


    # Methods to attach event handlers to the buttons, the application can than listen for presses.
    def startListeningForGreenRedButtons(self):
        with self._lock:
            if not self._listeningForGreenRedButton:
                GPIO.add_event_detect(Constants.GREEN_BUTTON_PIN, GPIO.RISING, callback=self.greenButtonPressed, bouncetime=Constants.BOUNCE_TIME)
                GPIO.add_event_detect(Constants.RED_BUTTON_PIN, GPIO.RISING, callback=self.redButtonPressed, bouncetime=Constants.BOUNCE_TIME)
                self._listeningForRedGreenButton = True


    def startListeningServiceButton(self):
        with self._lock:
            if not self._listeningForServiceButton:
                GPIO.add_event_detect(Constants.SERVICE_BUTTON_PIN, GPIO.BOTH, callback=self.serviceButtonPressedReleased, bouncetime=Constants.BOUNCE_TIME)
                self._listeningForServiceButton = True


    # Methods to remove event handlers
    def stopListeningForGreenRedButtons(self):
        with self._lock:
            if self._listeningForRedGreenButton:
                GPIO.remove_event_detect(Constants.GREEN_BUTTON_PIN)
                GPIO.remove_event_detect(Constants.RED_BUTTON_PIN)
                self._listeningForGreenRedButton = False


    def stopListeningServiceButton(self):
        with self._lock:
            if self._listeningForServiceButton:
                GPIO.remove_event_detect(Constants.SERVICE_BUTTON_PIN)
                self._listeningForServiceButton = False


    # Listeners for buttons
    def greenButtonPressed(self, channel):
        time.sleep(0.02)
        if not GPIO.input(Constants.GREEN_BUTTON_PIN):
            return
        if not self._lock.acquire(False) or self._serviceButtonPressed:
            return

        if self._greenRedButtonCallback != None:
            self._greenRedButtonCallback.greenButtonPressed()

        self._lock.release()

    def redButtonPressed(self, channel):
        time.sleep(0.02)
        if not GPIO.input(Constants.RED_BUTTON_PIN):
            return
        if not self._lock.acquire(False) or self._serviceButtonPressed:
            return

        if self._greenRedButtonCallback != None:
            self._greenRedButtonCallback.redButtonPressed()

        self._lock.release()
    

    def serviceButtonPressedReleased(self, channel):
        time.sleep(0.01)
        if not self._lock.acquire(False):
            return

        if GPIO.input(Constants.SERVICE_BUTTON_PIN):
            self._serviceButtonLastPressedTime = datetime.datetime.utcnow()
            self._serviceButtonPressed = True
        else:
            self._serviceButtonPressed = False
            if (datetime.datetime.utcnow() - self._serviceButtonLastPressedTime).seconds < Constants.LONG_BUTTON_PRESS_TIME:
                self._serviceButtonCallback.serviceButtonShortPressed()
            else:
                self._serviceButtonCallback.serviceButtonLongPressed()

        self._lock.release()


    # Methods to register callbacks
    def setGreenRedButtonCallback(self, greenRedButtonCallbackObject):
        with self._lock:
            self._greenRedButtonCallback = greenRedButtonCallbackObject


    def setServiceButtonCallback(self, callbackObject):
        with self._lock:
            self._serviceButtonCallback = callbackObject