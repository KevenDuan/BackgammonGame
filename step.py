import RPi.GPIO as GPIO
import time

class StepControl:
    def __init__(self):
        """
        step1: 13 and 15
        step2: 16 and 18
        step3: 36 and 38
        """
        # x轴
        self.IN1 = 13  # 连接到PUL+
        self.IN2 = 15  # 连接DIR+
        # y轴
        self.IN3 = 16  # 连接到PUL+
        self.IN4 = 18  # 连接DIR+
        # z轴
        self.IN5 = 36  # 连接到PUL+
        self.IN6 = 38  # 连接DIR+
        self.setup()

    def setup(self):
        GPIO.setwarnings(False)
        # 设置GPIO模式为BOARD
        GPIO.setmode(GPIO.BOARD)
        # 设置GPIO口为输出
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.IN5, GPIO.OUT)
        GPIO.setup(self.IN6, GPIO.OUT)

    # 定义发送脉冲函数
    def send_pulse(self, pur, dir, steps, direction):
        # 设置方向
        if direction: GPIO.output(dir, GPIO.HIGH)  # 正转
        else: GPIO.output(dir, GPIO.LOW)   # 反转

        # 发送脉冲信号
        for _ in range(steps):
            GPIO.output(pur, GPIO.HIGH)
            time.sleep(0.0001)  # 脉冲持续时间
            GPIO.output(pur, GPIO.LOW)
            time.sleep(0.0001)  # 脉冲间隔时间

    def x_backward(self, step):
        self.send_pulse(self.IN1, self.IN2, step, False)
        # self.clean()
    
    def x_forward(self, step):
        self.send_pulse(self.IN1, self.IN2, step, True)

    def y_forward(self, step):
        self.send_pulse(self.IN3, self.IN4, step, True)

    def y_backward(self, step):
        self.send_pulse(self.IN3, self.IN4, step, False)

    def clean(self):
        GPIO.cleanup()

    def down(self):
        self.send_pulse(self.IN5, self.IN6, 2000, False)

    def up(self):
        self.send_pulse(self.IN5, self.IN6, 2000, True)

if __name__ == "__main__":
    step = StepControl()
    # step.x_forward(1000)
    step.up()

    step.clean()

