import cv2
import numpy as np

hsv_low = np.array([0, 0, 0])
hsv_high = np.array([0, 0, 0])

def h_low(value):
    hsv_low[0] = value
def h_high(value):
    hsv_high[0] = value
def s_low(value):
    hsv_low[1] = value
def s_high(value):
    hsv_high[1] = value
def v_low(value):
    hsv_low[2] = value
def v_high(value):
    hsv_high[2] = value

cv2.namedWindow('image',cv2.WINDOW_AUTOSIZE)
# 可以自己设定初始值，最大值255不需要调节
cv2.createTrackbar('H low', 'image', 126, 255, h_low)
cv2.createTrackbar('H high', 'image', 255, 255, h_high)
cv2.createTrackbar('S low', 'image', 43, 255, s_low)
cv2.createTrackbar('S high', 'image', 255, 255, s_high)
cv2.createTrackbar('V low', 'image', 46, 255, v_low)
cv2.createTrackbar('V high', 'image', 255, 255, v_high)

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    while (True):
        # 开始用摄像头读数据，返回hx为true则表示读成功，frame为读的图像
        hx, frame = cap.read()
        # 初始化四边形检测器
        dst = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # BGR转HSV
        dst = cv2.inRange(dst, hsv_low, hsv_high) # 通过HSV的高低阈值，提取图像部分区域
        cv2.imshow('dst', dst)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放摄像头
    cap.release()

    # 结束所有窗口
    cv2.destroyAllWindows()
