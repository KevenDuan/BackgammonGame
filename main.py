import numpy as np
import quad_detector
import step
import cv2

cap = cv2.VideoCapture(0)

step = step.StepControl() # 初始化步进电机
quad_detector = quad_detector.QuadDetector(1000, 500, 200/600, 30, 6) # 初始化视觉类
point_axis = []
point_key = {}

while (True):
    # 开始用摄像头读数据，返回hx为true则表示读成功，frame为读的图像
    hx, frame = cap.read()
    # 初始化四边形检测器
    try:
        if len(point_axis) == 0:
            # 四边形检测结果
            vertices, scale_vertices, intersection = quad_detector.detect(frame)
            img_detected = quad_detector.draw(frame)  # 绘制检测结果
            # 显示摄像头图像，其中的video为窗口名称，frame为图像
            # cv2.imshow('detect', img_detected)
            point_axis = quad_detector.point_list
            point_key = quad_detector.point_key
    except Exception as e:
        print(e)

    print(point_key)
    machine_x, machine_y = quad_detector.colorDetect(frame)
    print(machine_x, machine_y)

    # cv2.imshow('img', frame)
    # # 监测键盘输入是否为q，为q则退出程序
    # if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q退出
    #     break

# 释放摄像头
cap.release()

# 结束所有窗口
cv2.destroyAllWindows()