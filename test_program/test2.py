import RPi.GPIO as GPIO
import time

class StepControl:
    def __init__(self):
        # 规定GPIO引脚
        # 第一个步进电机
        self.IN1 = 18      # 接PUL+
        self.IN2 = 15      # 接DIR+
        # 第二个步进电机
        self.IN3 = 16 # 接PUL+
        self.IN4 = 13 # 接DIR+
        self.setup()

    def microsecond_sleep(self, sleep_time=500):
        end_time = time.perf_counter() + (sleep_time - 0.8) / 1e6  # 0.8是时间补偿，需要根据自己PC的性能去实测
        while time.perf_counter() < end_time:
            pass
    
    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
        GPIO.setup(self.IN1, GPIO.OUT)      # Set pin's mode is output
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        
    def setStep(self, w1, w2, w3, w4):
        GPIO.output(self.IN1, w1)
        GPIO.output(self.IN2, w2)
        GPIO.output(self.IN3, w3)
        GPIO.output(self.IN4, w4)
    
    def y_backward(self, steps, delay=0.00001):  
        for i in range(0, steps):
            self.setStep(0, 1, 0, 1)
            time.sleep(delay)
            self.setStep(1, 0, 1, 0)
            time.sleep(delay)

    def y_forward(self, steps, delay=0.00001):  
        for i in range(0, steps):
            self.setStep(1, 0, 1, 0)
            time.sleep(delay)
            self.setStep(0, 0, 0, 0)
            time.sleep(delay)

    def x_forward(self, steps, delay=0.00001):  
        for i in range(0, steps):
            self.setStep(1, 0, 0, 1)
            time.sleep(delay)
            self.setStep(0, 0, 1, 0)
            time.sleep(delay)

    def x_backward(self, steps, delay=0.00001):  
        for i in range(0, steps):
            self.setStep(0, 1, 1, 0)
            time.sleep(delay)
            self.setStep(1, 0, 0, 0)
            time.sleep(delay)

    def stop(self):
        self.setStep(0, 0, 0, 0)
    
    def destroy(self):
        GPIO.cleanup() # 释放数据

if __name__ == "__main__":
    step = StepControl()
    step.x_forward(10000)