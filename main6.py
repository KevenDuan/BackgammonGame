import numpy as np
import quad_detector
import step
import cv2
import electromagnets
import time
import backgammon
import sys
import ledContorl

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


def black_chess_detection(frame):
    # 定义颜色范围（在HSV颜色空间中）
    dst2 = cv2.GaussianBlur(frame, (9, 9), 0)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 131])
    # 将帧转换为HSV颜色空间
    hsv_frame2 = cv2.cvtColor(dst2, cv2.COLOR_BGR2HSV)
    # 根据颜色范围创建掩膜
    black_mask = cv2.inRange(hsv_frame2, lower_black, upper_black)
    # 对掩膜进行形态学操作，以去除噪声
    kernel2 = np.ones((9, 9), np.uint8)
    # white_mask = cv2.dilate(white_mask, kernel2, iterations = 1)
    black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_OPEN, kernel2)
    cv2.imshow('black_inrange', black_mask)
    # 在原始帧中找到颜色区域并绘制方框
    contours, _ = cv2.findContours(black_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        color = ""
        if 2000 > cv2.contourArea(contour) > 200 and h * 1.25 > w and w * 1.25 > h:  # 设置最小区域面积以排除噪声
            if np.any(black_mask[y:y + h, x:x + w]):
                color = "black"
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                new_x, new_y = x + w//2, y + h//2
                for x, y in black_list:
                    if (x - 3 <= new_x <= x + 3) and (y - 3 <= new_y <= y + 3):
                        break
                else:
                    if len(black_list) < 5: black_list.append((new_x, new_y))

            cv2.putText(frame, color, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    return frame

def white_chess_detection(frame):
    # 定义颜色范围（在HSV颜色空间中）
    dst1 = cv2.GaussianBlur(frame, (9, 9), 0)
    lower_white = np.array([0, 0, 46])
    upper_white = np.array([180, 55, 255]) # 40~75

    # 将帧转换为HSV颜色空间
    hsv_frame1 = cv2.cvtColor(dst1, cv2.COLOR_BGR2HSV)

    # 根据颜色范围创建掩膜
    white_mask = cv2.inRange(hsv_frame1, lower_white, upper_white)

    # 对掩膜进行形态学操作，以去除噪声
    kernel1 = np.ones((9, 9), np.uint8)
    # white_mask = cv2.dilate(white_mask, kernel2, iterations = 1)
    white_mask = cv2.morphologyEx(white_mask, cv2.MORPH_OPEN, kernel1)

    cv2.imshow('white_inrange', white_mask)


    # 在原始帧中找到颜色区域并绘制方框
    contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        color = ""
        if 2000 > cv2.contourArea(contour) > 200 and h * 1.25 > w and w * 1.25 > h:  # 设置最小区域面积以排除噪声
            if np.any(white_mask[y:y + h, x:x + w]):
                color = "white"
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                new_x, new_y = x + w//2, y + h//2
                for x, y in new_white_list:
                    if (x - 3 <= new_x <= x + 3) and (y - 3 <= new_y <= y + 3):
                        break
                else:
                    if len(new_white_list) < 5: new_white_list.append((new_x, new_y))

            cv2.putText(frame, color, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    return frame


def move_white(pos):
    """
    控制机械臂将白色棋子移动到九宫格
    """
    # 从机械臂当前位置移动到白色棋子    
    sta = time.time()      
    while len(last_white_list) > 0 and len(point_axis) != 0:
        zip_axis = last_white_list.pop()
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
                print(f"time: {time.time() - sta - 4} s")
                led = ledContorl.Led()
                led.open()


                step.up() # 抬起电磁铁
                time.sleep(0.02)

                move(point_key[pos][0], point_key[pos][1], 300, -50)
                return

if __name__ == "__main__":
    # 打开摄像头
    cap = cv2.VideoCapture(0)

    quad_detector = quad_detector.QuadDetector(9999, 200, 200/600, 30, 6) # 初始化视觉类
    e = electromagnets.Electromagnets() # 初始化电磁铁
    gammon = backgammon.Backgammon() # 初始化三字棋算法类
    led = ledContorl.Led() # 初始化led灯

    point_axis = []
    black_list = [] # 存黑色棋子
    last_white_list = [] # 存白色棋子
    new_white_list = []

    point_key = {} # 用字典存九宫格的坐标
    step = step.StepControl() # 初始化步进电机

    #############裁剪部分###################
    up, down, l, r = 100, -80, 140, -120
    ###########根据摄像头进行更改############

    while True:
        hx, frame = cap.read()
        hx, frame = cap.read()
        hx, frame = cap.read()
        hx, frame = cap.read()
        hx, frame = cap.read()
        hx, frame = cap.read()
        frame = frame[up:down, l:r]

        while len(point_axis) < 9:
            try: # 把九宫格内的数据读取出来
                if len(point_axis) == 0:
                    # 四边形检测结果
                    vertices, scale_vertices, intersection = quad_detector.detect(frame) # 检测四边形方框
                    img_detected = quad_detector.draw(frame)  # 绘制检测结果
                    # 显示摄像头图像，其中的video为窗口名称，frame为图像
                    cv2.imshow('detect', img_detected)

                    point_axis = quad_detector.point_list
                    point_key = quad_detector.point_key

            except Exception as e:
                print(e)
        
        while len(last_white_list) < 5: # 读取第一次白色的位置
                hx, frame = cap.read()
                hx, frame = cap.read()
                hx, frame = cap.read()
                hx, frame = cap.read()
                hx, frame = cap.read()
                hx, frame = cap.read()
                frame = frame[up:down, l:r]
                quad_detector.chess_detection(frame)
                last_white_list = quad_detector.white_list
                # print(white_list)
        # 显示出棋盘的区域
        vertices = sorted(vertices, key=lambda x:x[0] + x[1])
        x_range = [vertices[0][0], vertices[-1][0]]
        y_range = [vertices[0][1], vertices[-1][1]]

        while True: # 检测人下的黑棋
            hx, frame = cap.read()
            hx, frame = cap.read()
            hx, frame = cap.read()
            hx, frame = cap.read()
            hx, frame = cap.read()
            hx, frame = cap.read()
            frame = frame[up:down, l:r]

            black_list = [] # 读取前需要清空
            black_chess_detection(frame) # 重新检测黑色棋子
            # print('black_list: ', black_list)
            # print('white_list:', white_list)
            # print(point_key)

            input('Are you ok?')
            """
            检测人是否移动了装置的棋子
            """
            white_chess_detection(frame)
            for i in range(len(gammon.board)):
                for j in range(len(gammon.board[0])):
                    if gammon.board[i][j] == 'O':
                        for x, y in new_white_list:
                            pos = gammon.axis_turn_key(x, y)
                            key_x, key_y = point_key()
                            if key_x - 20 < x < key_x + 20 and key_y - 20 < y < key_y + 20:
                                continue
                            else: # 移动棋子到原来的位置
                                for old_x, old_y in last_white_list:
                                    for new_x, new_y in new_white_list:
                                        if old_x - 10 < x < old_x + 10 and old_y - 10 < y < old_y + 10:
                                            continue
                                        else:
                                            while move(new_x, new_y, key_x, key_y):
                                                print('正常校准中...')



            for b_x, b_y in black_list:
                for key, value in point_key.items():
                    x, y = value[0], value[1]
                    t = gammon.key_turn_axis(key)
                    if x - 20 < b_x < x + 20 and y - 20 < b_y < y + 20 and gammon.board[t[0]][t[1]] == ' ':
                        print(f'{key}位置存在黑棋')
                        gammon.board[t[0]][t[1]] = 'X'
                        xx, yy = gammon.find_best_move(gammon.board)
                        pos = gammon.axis_turn_key(xx, yy) # pos位置为给出的最优下点

                        
                        move_white(pos)
                        gammon.board[xx][yy] = 'O'

                        if gammon.evaluate(gammon.board) == 10:
                            print('machine win!')
                            sys.exit()