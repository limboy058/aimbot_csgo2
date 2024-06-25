from multiprocessing import Process, Array, Value
from ultralytics import YOLO
from pynput import keyboard
from tkinter import *
from tkinter.ttk import *
import ctypes
import time
import matplotlib.pyplot as plt
import os
os.getcwd()
os.add_dll_directory(
    'C:\\Users\\Limbo\\Desktop\\code\\2024.3\\AI\\lab3\\demo\\DXGI.pyd')
from ctypes import windll
import cv2
import numpy as np
import sys
sys.path.append('C:\\Users\\Limbo\\Desktop\\code\\2024.3\\AI\\lab3\\demo')
import DXGI
g = DXGI.capture(780,220,1780,1220)  # 屏幕左上角 到 右下角  （x1, y1 ,x2 ,y2)

bbox = (780,220,1780,1220)  #(1000*1000)

try:
    root = os.path.abspath(os.path.dirname(__file__))
    driver = ctypes.CDLL(f'{root}/logitech.driver.dll')
    ok = driver.device_open() == 1  # 该驱动每个进程可打开一个实例
    if not ok:
        print('Error, GHUB or LGS driver not found')
except FileNotFoundError:
    print(f'Error, DLL file not found')


class Logitech:

    class mouse:
        """
        code: 1:左键, 2:中键, 3:右键
        """

        @staticmethod
        def press(code):
            if not ok:
                return
            driver.mouse_down(code)

        @staticmethod
        def release(code):
            if not ok:
                return
            driver.mouse_up(code)

        @staticmethod
        def click(code):
            if not ok:
                return
            driver.mouse_down(code)
            driver.mouse_up(code)

        @staticmethod
        def scroll(a):
            """
            a:没搞明白
            """
            if not ok:
                return
            driver.scroll(a)

        @staticmethod
        def move(x, y):
            """
            相对移动, 绝对移动需配合 pywin32 的 win32gui 中的 GetCursorPos 计算位置
            pip install pywin32 -i https://pypi.tuna.tsinghua.edu.cn/simple
            x: 水平移动的方向和距离, 正数向右, 负数向左
            y: 垂直移动的方向和距离
            """
            if not ok:
                return
            if x == 0 and y == 0:
                return
            driver.moveR(x, y, True)


def get_key(yes):
    def on_press(key):
        try:
            if key.char == ']' and yes.value == 0:
                print('截一张图')
                yes.value = 1
            elif key.char == ']' and yes.value == 1:
                print('关闭外挂')
                yes.value = 0
        except AttributeError:
            i=1

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()



def get_data(yes, bodys, heads):
    while (1):
        if yes.value == 0:
            continue

        im = g.cap()
        #im = np.array(im)
        #im = cv2.resize(im, dsize=(500, 500),interpolation=cv2.INTER_LINEAR)
        # cv2.imshow('c', im)
        # cv2.waitKey(1)
        plt.imshow(im)
        plt.show()
        # name=str(int(time.time()))

        # cv2.imwrite('./pic/'+name+'.png', im)
        yes.value=0
        print("done")
        



if __name__ == '__main__':
    heads = Array('f', 40, lock=False)
    bodys = Array('f', 40, lock=False)
    yes = Value('i', 0, lock=False)

    Get_key = Process(target=get_key, args=(yes, ))
    Get_data = Process(target=get_data, args=(yes, bodys, heads))
    

    Get_key.start()
    Get_data.start()


    Get_key.join()
    Get_data.join()

