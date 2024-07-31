import time
import board
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

i2c = board.I2C()  # uses board.SCL and board.SDA
pca = PCA9685(i2c)
pca.frequency = 50

def setAngle(bone1, bone2, bone3, claw=0, head=90):
    # bone2: 90 ~ 180
    servo2.angle = bone1
    servo3.angle = 270 - bone2
    servo4.angle = bone3
    servo1.angle = claw
    servo5.angle = head

servo1 = servo.Servo(pca.channels[7])
servo2 = servo.Servo(pca.channels[8])
servo3 = servo.Servo(pca.channels[9])
servo4 = servo.Servo(pca.channels[10])
servo5 = servo.Servo(pca.channels[11])

# setup()
setAngle(145, 90, 125, 0)

for i in range(90, 180):
    angle = (180 - i) // 2 + 90
    setAngle(angle + 15, i, angle - 5)
    time.sleep(0.2)