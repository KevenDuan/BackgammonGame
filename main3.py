import numpy as np
import quad_detector
import step
import cv2
import electromagnets
import sys
import time

def move(now_x, now_y, dist_x, dist_y):
    """
    从(now_x, now_y) -> (dist_x, dist_y)
    """
    step.setup()
    abs_x = abs(now_x - dist_x) * 50
    abs_y = abs(now_y - dist_y) * 50
    if abs_x <= 5 and abs_y <= 5:
        step.y_backward(3000)
        print('sucessfully!')
        return True
    if dist_x > now_x:
         step.x_forward(abs_x)
    else: step.x_backward(abs_x)

    if dist_y > now_y:
        step.y_backward(abs_y)
    else: step.y_forward(abs_y)
    return False

if __name__ == "__main__":
    # 打开摄像头
    cap = cv2.VideoCapture(0)

    quad_detector = quad_detector.QuadDetector(9999, 200, 200/600, 30, 6) # 初始化视觉类
    point_axis = []
    black_list = [] # 存黑色棋子
    white_list = [] # 存白色棋子
    white_cnt, black_cnt = 0, 0

    point_key = {} # 用字典存九宫格的坐标
    ox, oy = 0, 0
    # 回到初始位置
    step = step.StepControl() # 初始化步进电机

    #############裁剪部分###################
    up, down, l, r = 100, -80, 140, -120
    ###########根据摄像头进行更改############

    while True:
        e = electromagnets.Electromagnets() # 初始化电磁铁
        hx, frame = cap.read()
        hx, frame = cap.read()
        hx, frame = cap.read()
        hx, frame = cap.read()
        hx, frame = cap.read()
        hx, frame = cap.read()
        frame = frame[up:down, l:r]

        try:
            if len(point_axis) == 0:
                # 四边形检测结果
                vertices, scale_vertices, intersection = quad_detector.detect(frame) # 检测四边形方框
                img_detected = quad_detector.draw(frame)  # 绘制检测结果
                # 显示摄像头图像，其中的video为窗口名称，frame为图像
                cv2.imshow('detect', img_detected)

                point_axis = quad_detector.point_list
                point_key = quad_detector.point_key

            if len(black_list) == 0:
                quad_detector.chess_detection(frame)
                black_list = quad_detector.black_list

            if len(white_list) == 0:
                quad_detector.chess_detection(frame)
                white_list = quad_detector.white_list
                
            black_list = quad_detector.black_list
            white_list = quad_detector.white_list
            
        except Exception as e:
            print(e)
        
        print(point_key) # 打印出坐标信息
        # print(point_axis)
        
        machine_x, machine_y = quad_detector.detectMachineArm(frame)
        print('axis:', (machine_x, machine_y))

        # 从机械臂当前位置移动到白色棋子        
        while len(white_list) > 0 and len(point_axis) != 0:
            
            if white_cnt >= 2: break
            zip_axis = white_list.pop()
            white_x, white_y = zip_axis[0], zip_axis[1]
            print('white_axis: ', (white_x, white_y))
            while True: 
                e = electromagnets.Electromagnets()
                hx, frame = cap.read()
                hx, frame = cap.read()
                hx, frame = cap.read()
                hx, frame = cap.read()
                hx, frame = cap.read()
                hx, frame = cap.read()
                frame = frame[up:down, l:r]
                machine_x, machine_y = quad_detector.detectMachineArm(frame)
                if move(machine_x, machine_y, white_x, white_y):
                    step.down() # 落下电磁铁
                    time.sleep(0.02)
                    e.open() # 启动电磁铁吸取
                    print('拿棋子成功')
                    time.sleep(0.02)

                    step.up() # 抬起电磁铁
                    time.sleep(0.02)
                    break
            
            # 从白色棋子移动到指定号九宫格
            pos = int(input('please input postion: '))
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
                if move(machine_x, machine_y, point_key[pos][0], point_key[pos][1]):
                    step.down() # 落下电磁铁
                    time.sleep(0.02)
                    e.close() # 释放吸力
                    time.sleep(0.02)
                    print('放棋子成功')
                    step.up() # 抬起电磁铁
                    time.sleep(0.02)

                    white_cnt += 1

                    break
            
        # 从机械臂当前位置移动到黑色棋子        
        while len(black_list) > 0 and len(point_axis) != 0:
            if black_cnt >= 2: break
            zip_axis = black_list.pop()
            black_x, black_y = zip_axis[0], zip_axis[1]
            print('white_axis: ', (black_x, black_y))
            while True: 
                e = electromagnets.Electromagnets()
                hx, frame = cap.read()
                hx, frame = cap.read()
                hx, frame = cap.read()
                hx, frame = cap.read()
                hx, frame = cap.read()
                hx, frame = cap.read()
                frame = frame[up:down, l:r]
                machine_x, machine_y = quad_detector.detectMachineArm(frame)
                if move(machine_x, machine_y, black_x, black_y):
                    step.down() # 落下电磁铁
                    time.sleep(0.02)
                    e.open() # 启动电磁铁吸取
                    print('拿棋子成功')
                    time.sleep(0.02)

                    step.up() # 抬起电磁铁
                    time.sleep(0.02)
                    break
            
            # 从黑色棋子移动到指定号九宫格
            pos = int(input('please input postion: '))
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
                if move(machine_x, machine_y, point_key[pos][0], point_key[pos][1]):
                    step.down() # 落下电磁铁
                    time.sleep(0.02)
                    e.close() # 释放吸力
                    time.sleep(0.02)
                    print('放棋子成功')

                    step.up() # 抬起电磁铁
                    time.sleep(0.02)

                    black_cnt += 1

                    break

 