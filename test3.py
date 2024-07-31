import cv2
import numpy as np

def detectMachineArm(img):
    """
    @img: 需要识别的图像
    @return: 返回识别到机械臂的坐标(x, y)
    如果没有识别到返回 (-1, -1)
    """
    dst = cv2.GaussianBlur(img, (25, 25), 0)

    hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)  # 转化成HSV图像
    # 颜色二值化筛选处理
    inRange_hsv_green = cv2.inRange(hsv, np.array([127, 0, 0]), np.array([255, 255, 255]))
    cv2.imshow('inrange_hsv_re', inRange_hsv_green)
    try:
        # 找中心点
        cnts1 = cv2.findContours(inRange_hsv_green.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        c1 = max(cnts1, key=cv2.contourArea)
        if cv2.contourArea(c1) < 100:
            print('not find machine arm')
            return -1, -1
        M = cv2.moments(c1)
        cX1 = int(M["m10"] / M["m00"])
        cY1 = int(M["m01"] / M["m00"])
        # cv2.circle(img, (cX1, cY1), 3, (0, 0, 255), -1)
        rect = cv2.minAreaRect(c1)
        box = cv2.boxPoints(rect)
        cv2.drawContours(img, [np.intp(box)], -1, (0, 0, 255), 2)
        cv2.imshow('camera', img)
        if cv2.waitKey() == ord('q'):
            return -1, -1
        return cX1, cY1
    except:
        cv2.waitKey()
        print('not find machine arm')
        return -1, -1

cap = cv2.VideoCapture(0)
while (True):
    # 开始用摄像头读数据，返回hx为true则表示读成功，frame为读的图像
    hx, frame = cap.read()

    # print(point_key)
    x, y = detectMachineArm(frame)
    print(x, y)

cv2.destroyAllWindows()