import RPi.GPIO as GPIO
import time

# 设置GPIO模式为BCM
GPIO.setmode(GPIO.BOARD)

PULSE_PIN = 36  # 连接到PUL+
DIRECTION_PIN = 38  # 连接DIR+



# 设置GPIO口为输出
GPIO.setup(PULSE_PIN, GPIO.OUT)
GPIO.setup(DIRECTION_PIN, GPIO.OUT)

# 定义发送脉冲函数
def send_pulse(steps, direction):
    # 设置方向
    if direction:
        GPIO.output(DIRECTION_PIN, GPIO.HIGH)  # 正转
    else:
        GPIO.output(DIRECTION_PIN, GPIO.LOW)   # 反转

    # 发送脉冲信号
    for _ in range(steps):
        GPIO.output(PULSE_PIN, GPIO.HIGH)
        time.sleep(0.0001)  # 脉冲持续时间
        GPIO.output(PULSE_PIN, GPIO.LOW)
        time.sleep(0.0001)  # 脉冲间隔时间

# 控制电机正转6400步
send_pulse(1000, False)

# 等待一段时间
# time.sleep(1)

# # 控制电机反转6400步
# send_pulse(2400, False)

# 清理GPIO资源
GPIO.cleanup()
