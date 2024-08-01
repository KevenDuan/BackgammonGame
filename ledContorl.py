import RPi.GPIO as GPIO
import time

class Led:
    def __init__(self):
        self.pin = 7
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)

    def open(self):
        for _ in range(2):  
            GPIO.output(7, False)
            time.sleep(0.5)
            GPIO.output(7, True)
            time.sleep(0.5)

if __name__ == "__main__":
    led = Led()
    led.open()
    
