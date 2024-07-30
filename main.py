import numpy as np
import quad_detector
import step
import cv2
import time

cap = cv2.VideoCapture(0)

step = step.StepControl() # 初始化步进电机
quad_detector = quad_detector.QuadDetector(1000, 500, 200/600, 30, 6) # 初始化视觉类
point_axis = []
point_key = {}

def move(now_x, now_y, dist_x, dist_y):
    step.setup()
    """
    从(now_x, now_y) -> (dist_x, dist_y)
    """
    abs_x = abs(now_x - dist_x) * 125
    abs_y = abs(now_y - dist_y) * 125
    if abs_x < 8 and abs_y < 8: return True
    if dist_x > now_x:
         step.x_forward(abs_x)
    else: step.x_backward(abs_x)

    if dist_y > now_y:
        step.y_backward(abs_y)
    else: step.y_forward(abs_y)
    step.destroy()
    return False

while (True):
    # 开始用摄像头读数据，返回hx为true则表示读成功，frame为读的图像
    hx, frame = cap.read()
    hx, frame = cap.read()
    hx, frame = cap.read()
    hx, frame = cap.read()
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
    print(point_axis)
    while True:
        a = int(input('input: '))
        while True:
            hx, frame = cap.read()
            hx, frame = cap.read()
            hx, frame = cap.read()
            hx, frame = cap.read()
            hx, frame = cap.read()
            machine_x, machine_y = quad_detector.detectMachineArm(frame)
            print('axis:', (machine_x, machine_y))
            if machine_x != machine_y != -1:
                if move(machine_x, machine_y, point_key[a][0], point_key[a][1]):
                    break
    # black_x, black_y = quad_detector.detectBlack(frame)
    # print(black_x, black_y)

    # cv2.imshow('img', frame)
    # # # # 监测键盘输入是否为q，为q则退出程序
    # if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q退出
    #      break

# # 释放摄像头
# cap.release()

# # 结束所有窗口
# cv2.destroyAllWindows()