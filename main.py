import numpy as np
import quad_detector
import step
import cv2
import electromagnets
import sys

cap = cv2.VideoCapture(0)

step = step.StepControl() # 初始化步进电机
quad_detector = quad_detector.QuadDetector(1000, 200, 200/600, 30, 6) # 初始化视觉类
point_axis = []
black_list = []
point_key = {}
ox, oy = 0, 0
# 回到初始位置
step.x_forward(24000)

def move(now_x, now_y, dist_x, dist_y):
    step.setup()
    """
    从(now_x, now_y) -> (dist_x, dist_y)
    """
    abs_x = abs(now_x - dist_x) * 125
    abs_y = abs(now_y - dist_y) * 125
    if abs_x <= 1 and abs_y <= 1:
        step.y_backward(4500)
        print('sucessfully!')
        return True
    if dist_x > now_x:
         step.x_forward(abs_x)
    else: step.x_backward(abs_x)

    if dist_y > now_y:
        step.y_backward(abs_y)
    else: step.y_forward(abs_y)
    step.destroy()
    return False

#######################################
up, down, l, r = 160, -150, 210, -170
#######################################
while True:
    # e.open()
    # 开始用摄像头读数据，返回hx为true则表示读成功，frame为读的图像
    hx, frame = cap.read()
    hx, frame = cap.read()
    hx, frame = cap.read()
    hx, frame = cap.read()
    hx, frame = cap.read()
    hx, frame = cap.read()
    frame = frame[up:down, l:r]

    # 初始化四边形检测器
    try:
        if len(point_axis) == 0:
            # 四边形检测结果
            vertices, scale_vertices, intersection = quad_detector.detect(frame)
            img_detected = quad_detector.draw(frame)  # 绘制检测结果
            # 显示摄像头图像，其中的video为窗口名称，frame为图像
            cv2.imshow('detect', img_detected)
            point_axis = quad_detector.point_list
            point_key = quad_detector.point_key
            black_list = quad_detector.black_list
        
    except Exception as e:
        print(e)
    
    # print(point_key)
    # print(point_axis)
    
    machine_x, machine_y = quad_detector.detectMachineArm(frame)
    print('axis:', (machine_x, machine_y))

    # move(machine_x, machine_y, point_key[5][0], point_key[5][1])
    # if abs(machine_x - point_key[5][0]) == 0 and abs(machine_y - point_key[5][1]) == 0:
    #     e.close()
    #     move(point_key[5][0], point_key[5][1], ox, oy)
    #     print('sucesfully!')
    #     break
    
    if len(black_list) > 0:
        black_x, black_y = black_list[0][0], black_list[0][1]
        print('black_axis: ', (black_x, black_y))
        while True: 
            hx, frame = cap.read()
            hx, frame = cap.read()
            hx, frame = cap.read()
            hx, frame = cap.read()
            hx, frame = cap.read()
            hx, frame = cap.read()
            frame = frame[up:down, l:r]
            machine_x, machine_y = quad_detector.detectMachineArm(frame)
            if move(machine_x, machine_y, black_x, black_y):
                print('拿棋子成功')
                e = electromagnets.Electromagnets()
                e.open()
                break

        while True:
            e = electromagnets.Electromagnets()
            e.open()
            hx, frame = cap.read()
            hx, frame = cap.read()
            hx, frame = cap.read()
            hx, frame = cap.read()
            hx, frame = cap.read()
            hx, frame = cap.read()
            frame = frame[up:down, l:r]
            machine_x, machine_y = quad_detector.detectMachineArm(frame)
            if move(machine_x, machine_y, point_key[5][0], point_key[5][1]):
                print('放棋子成功')
                e = electromagnets.Electromagnets()
                e.close()
                break

    print('####################')
    if move(point_key[5][0], point_key[5][1], ox, oy):
        ('**************************')
        sys.exit()
    else:
        sys.exit()

    # while True:
    #     a = int(input('input: '))
    #     while True:
    #         hx, frame = cap.read()
    #         hx, frame = cap.read()
    #         hx, frame = cap.read()
    #         hx, frame = cap.read()
    #         hx, frame = cap.read()
    #         frame = frame[up:down, l:r]
    #         machine_x, machine_y = quad_detector.detectMachineArm(frame)
    #         print('axis:', (machine_x, machine_y))
    #         if machine_x != machine_y != -1:
    #             if move(machine_x, machine_y, point_key[a][0], point_key[a][1]):
    #                 break 

#     cv2.imshow('img', frame)
#     # # # 监测键盘输入是否为q，为q则退出程序
#     if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q退出
#          break

# # 释放摄像头
# cap.release()

# # 结束所有窗口
# cv2.destroyAllWindows()