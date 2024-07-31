import RPi.GPIO as GPIO
from time import sleep
import sys

class Electromagnets:
    def __init__(self):    
        self.relay_pin = 11
        self.relay_state = False
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False) 
        GPIO.setup(self.relay_pin, GPIO.OUT)   

    def close(self):
        self.setup()
        GPIO.output(self.relay_pin, GPIO.LOW)
        # self.clean()

    def open(self):
        self.setup()
        GPIO.output(self.relay_pin, GPIO.HIGH)
        # self.clean()

    def clean(self):
        GPIO.cleanup()

if __name__ == "__main__":
    e = Electromagnets()
    while True:
        # e.open()
        # sleep(1)
        # e.close()
        # sleep(1)
        # e.clean()
        e.close()