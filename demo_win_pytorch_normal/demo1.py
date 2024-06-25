# 第一版
# 使用PIL截图
# 使用pydirectinput 进行鼠标操控
# 使用tkinter绘制

from ultralytics import YOLO
from PIL import ImageGrab


import pydirectinput
import pyautogui
#pyautogui.FAILSAFE=False
import time
from tkinter import *
from tkinter.ttk import *
import ctypes
from pynput import keyboard
import win32api
yes=0
bbox = (670, 360, 1860, 1080)  #(1190x720)
pth="C:\\Users\\Limbo\\Desktop\\code\\2024.3\\AI\\lab3\\best.pt"
model = YOLO(pth)
heads=[]
bodys=[]

print(pydirectinput.size())


def move_mouse():
    p = pydirectinput.position()
    print(p)

    global heads,bodys
    heads = sorted(heads, key=lambda x: abs((x[0]+x[2])/2-1280))
    bodys = sorted(bodys, key=lambda x: abs((x[0]+x[2])/2-1280))

    if len(heads)>=1:
        # print(heads)
        # print((heads[0][0]+heads[0][2])/2, (heads[0][1]+heads[0][3])/2)
        pydirectinput.moveRel(int((heads[0][0]+heads[0][2])/2+bbox[0]-1280), int((heads[0][1]+heads[0][3])/2+bbox[1]-720), duration=0.001,relative=True)
        #pyautogui.moveTo((heads[0][0]+heads[0][2])/2+bbox[0], (heads[0][1]+heads[0][3])/2+bbox[1],0.5,pyautogui.easeInOutQuad)
    elif len(bodys)>=1:
        # print(bodys)
        # print((bodys[0][0]+bodys[0][2])/2, (bodys[0][1]+bodys[0][3])/2)
        pydirectinput.moveRel(int((bodys[0][0]+bodys[0][2])/2+bbox[0]-1280), int((bodys[0][1]+bodys[0][3])/2+bbox[1]-720), duration=0.02,relative=True)
        #pyautogui.moveTo((bodys[0][0]+bodys[0][2])/2+bbox[0], (bodys[0][1]+bodys[0][3])/2+bbox[1],0.5,pyautogui.easeInOutQuad )


def get_data():
    heads.clear()
    bodys.clear()
    im = ImageGrab.grab(bbox).resize((320, 320))
    results=model.predict(source=im,verbose=False,conf=0.5)
    for i in results:
        b=i.cpu().boxes
        for idx in range(len(b.cls)):
            if(b.cls[idx]==1):
                tup=tuple(b.xyxy[idx].numpy())
                heads.append((tup[0]/320*1190,tup[1]/320*720,tup[2]/320*1190,tup[3]/320*720))
            else:
                tup=tuple(b.xyxy[idx].numpy())
                bodys.append((tup[0]/320*1190,tup[1]/320*720,tup[2]/320*1190,tup[3]/320*720))

def draw_circle():
    get_data()
    move_mouse()
    canvas.delete("all")  # 删除先前的所有图案
    canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill=TRANSCOLOUR, outline=TRANSCOLOUR)

    
    for b in bodys:
        canvas.create_rectangle(b[0],b[1],b[2],b[3],fill=TRANSCOLOUR,outline='blue')
    for h in heads:
        canvas.create_rectangle(h[0],h[1],h[2],h[3],fill=TRANSCOLOUR,outline='red')


def update_circle():
    draw_circle()
    tk.after(20, update_circle)




if __name__=='__main__':

    # while 1:
    #     get_data()
    #     move_mouse()
    #     #time.sleep(0.01)

    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0)
    tk = Tk()
    tk.tk.call('tk', 'scaling', ScaleFactor/75)
    TRANSCOLOUR = 'gray'
    screen_width = tk.winfo_screenwidth()
    screen_height = tk.winfo_screenheight()
    print(screen_width,screen_height)
    #tk.geometry("%dx%d+0+0" % (screen_width, screen_height))
    tk.attributes("-alpha", 1)
    tk.geometry('1190x720+670+360')
    tk.overrideredirect(True)
    tk.wm_attributes('-transparentcolor', TRANSCOLOUR)
    tk.attributes("-topmost",True)

    canvas = Canvas(tk)
    canvas.pack(fill=BOTH, expand=Y)

    update_circle()
    tk.mainloop()