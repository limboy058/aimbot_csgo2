# 测试使用dxgi和mss库哪个速度最快


import os
import time

os.getcwd()
os.add_dll_directory('C:\\Users\\Limbo\\Desktop\\code\\2024.3\\AI\\lab3\\demo_win_pytorch_normal\\DXGI.pyd')
#from ctypes import windll
import cv2
import numpy as np
# windll.winmm.timeBeginPeriod(1)
# stop = windll.kernel32.Sleep
import sys
sys.path.append('C:\\Users\\Limbo\\Desktop\\code\\2024.3\\AI\\lab3\\demo_win_pytorch_normal')
import mss
m=mss.mss()


import DXGI
g = DXGI.capture(780,220,1780,1220)  # 屏幕左上角 到 右下角  （x1, y1 ,x2 ,y2)

rect = (780,220,1780,1220)


time_used=0
for i in range(100):
    current_time = time.time()
    img = g.cap()
    # img = np.array(img)
    # img = cv2.resize(img, dsize=(640, 640))
    last_time = time.time()
    time_used += last_time - current_time

    # cv2.imshow('c', img)
    # cv2.waitKey(1)
print(time_used/100)

time_used=0
for i in range(100):
    current_time = time.time()
    img=m.grab(rect)
    # img = np.array(img)
    # img = cv2.resize(img, dsize=(640, 640))
    # img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    last_time = time.time()
    time_used += last_time - current_time

    # cv2.imshow('c', img)
    # cv2.waitKey(1)
print(time_used/100)
