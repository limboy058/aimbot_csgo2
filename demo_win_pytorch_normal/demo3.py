# 第三版

# 主要优化：使用DXGI进行快速截图
# 主要优化：使用罗技鼠标驱动ddl进行移动
# 主要优化：使用多进程处理，使用共享内存，将绘制操作独立出来，将延迟降到最低

from multiprocessing import Process, Array, Value
from ultralytics import YOLO
from pynput import keyboard
from tkinter import *
from tkinter.ttk import *
import ctypes
import time
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
g = DXGI.capture(670, 360, 1860, 1080)  # 屏幕左上角 到 右下角  （x1, y1 ,x2 ,y2)

bbox = (670, 360, 1860, 1080)  #(1190x720)

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
                print('开启外挂')
                yes.value = 1
            elif key.char == ']' and yes.value == 1:
                print('关闭外挂')
                yes.value = 0
        except AttributeError:
            i=1

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def draw_screen(yes,bodys,heads):
    def draw_circle():
        canvas.delete("all")  # 删除先前的所有图案
        canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill=TRANSCOLOUR, outline=TRANSCOLOUR)
        for i in range(0,40,4):
            if bodys[i]==0 and bodys[i+1]==0:
                break
            canvas.create_rectangle(bodys[i],bodys[i+1],bodys[i+2],bodys[i+3],fill=TRANSCOLOUR,outline='blue')
        for i in range(0,40,4):
            if bodys[i]==0 and bodys[i+1]==0:
                break
            canvas.create_rectangle(heads[i],heads[i+1],heads[i+2],heads[i+3],fill=TRANSCOLOUR,outline='red')

    def update_circle():
        draw_circle()
        tk.after(10, update_circle)

    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
    tk = Tk()
    tk.tk.call('tk', 'scaling', ScaleFactor/75)
    TRANSCOLOUR = 'gray'
    screen_width = tk.winfo_screenwidth()
    screen_height = tk.winfo_screenheight()
    print(screen_width,screen_height)
    tk.attributes("-alpha", 1)
    tk.geometry('1190x720+670+360')
    tk.overrideredirect(True)
    tk.wm_attributes('-transparentcolor', TRANSCOLOUR)
    tk.attributes("-topmost",True)
    canvas = Canvas(tk)
    canvas.pack(fill=BOTH, expand=Y)
    update_circle()
    tk.mainloop()


def movemouse(x, y):
    Logitech.mouse.move(int(0.7*x), int(0.7*y))
    Logitech.mouse.move(int(0.2*x), int(0.2*y))
    Logitech.mouse.move(int(0.1*x),int( 0.1*y))


def get_data(yes, bodys, heads):
    pth = "C:\\Users\\Limbo\\Desktop\\code\\2024.3\\AI\\lab3\\best.pt"
    model = YOLO(pth)
    cnt = 0
    t1 = time.time()
    while (1):
        if yes.value == 0:
            time.sleep(1)
            continue
        elif cnt == 0:
            t1 = time.time()
        cnt += 1
        im = g.cap()
        im = np.array(im)
        im = cv2.resize(im, dsize=(320, 320))
        im = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)

        results = model.predict(source=im, verbose=False, conf=0.5)
        head_cnt = 0
        body_cnt = 0
        for i in results:
            b = i.cpu().boxes
            for idx in range(len(b.cls)):
                if (b.cls[idx] == 1):
                    tup = tuple(b.xyxy[idx].numpy())
                    heads[head_cnt * 4] = tup[0] / 320 * 1190
                    heads[head_cnt * 4 + 1] = tup[1] / 320 * 720
                    heads[head_cnt * 4 + 2] = tup[2] / 320 * 1190
                    heads[head_cnt * 4 + 3] = tup[3] / 320 * 720
                    head_cnt += 1
                else:
                    tup = tuple(b.xyxy[idx].numpy())
                    bodys[body_cnt * 4] = tup[0] / 320 * 1190
                    bodys[body_cnt * 4 + 1] = tup[1] / 320 * 720
                    bodys[body_cnt * 4 + 2] = tup[2] / 320 * 1190
                    bodys[body_cnt * 4 + 3] = tup[3] / 320 * 720
                    body_cnt += 1

        heads[head_cnt * 4] = 0
        heads[head_cnt * 4 + 1] = 0
        heads[head_cnt * 4 + 2] = 0
        heads[head_cnt * 4 + 3] = 0
        bodys[body_cnt * 4] = 0
        bodys[body_cnt * 4 + 1] = 0
        bodys[body_cnt * 4 + 2] = 0
        bodys[body_cnt * 4 + 3] = 0

        if head_cnt >= 1:
            target = 0
            dis = abs((heads[target] + heads[target + 2]) / 2 + bbox[0] - 1280)
            for i in range(1, head_cnt):
                dis2 = abs((heads[i] + heads[i + 2]) / 2 + bbox[0] - 1280)
                if dis2 < dis:
                    dis = dis2
                    target = i
            movemouse(
                int((heads[target] + heads[target + 2]) / 2 + bbox[0] - 1280),
                int((heads[target + 1] + heads[target + 3]) / 2 + bbox[1] -
                    720))
        elif body_cnt >= 1:
            target = 0
            dis = abs((bodys[target] + bodys[target + 2]) / 2 + bbox[0] - 1280)
            for i in range(1, body_cnt):
                dis2 = abs((bodys[i] + bodys[i + 2]) / 2 + bbox[0] - 1280)
                if dis2 < dis:
                    dis = dis2
                    target = i
            movemouse(
                int((bodys[target] + bodys[target + 2]) / 2 + bbox[0] - 1280),
                int((bodys[target + 1] + bodys[target + 3]) / 2 + bbox[1] -
                    720))

        if yes.value == 0:
            t2 = time.time()
            print("计算了%d帧,检算帧率为%f" % (cnt, cnt / (t2 - t1)))
            cnt=0




if __name__ == '__main__':
    heads = Array('f', 40, lock=False)
    bodys = Array('f', 40, lock=False)
    yes = Value('i', 0, lock=False)

    Get_key = Process(target=get_key, args=(yes, ))
    Get_data = Process(target=get_data, args=(yes, bodys, heads))
    Draw_screen = Process(target=draw_screen, args=(yes, bodys, heads))

    Get_key.start()
    Get_data.start()
    Draw_screen.start()

    Get_key.join()
    Get_data.join()
    Draw_screen.join()
