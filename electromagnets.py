import RPi.GPIO as GPIO
import sys

class Electromagnets:
    def __init__(self):    
        self.relay_pin = 11  
        self.relay_state = False

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False) 
        GPIO.setup(self.relay_pin, GPIO.OUT)   

    def close(self):
         GPIO.output(self.relay_pin, GPIO.LOW)

    def open(self):
         GPIO.output(self.relay_pin, GPIO.HIGH)

if __name__ == "__main__":
    e = Electromagnets()
    while True:
        e.close()