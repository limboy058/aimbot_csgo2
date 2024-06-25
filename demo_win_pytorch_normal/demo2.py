# 第二版
# 使用PIL截图
# 使用pydirectinput 进行鼠标操控
# 使用tkinter绘制

# 使用pynput检测键盘输入，实现快捷键可以设置外挂功能


from multiprocessing import Process, Manager
from ultralytics import YOLO
from pynput import keyboard
import pydirectinput
from tkinter import *
from tkinter.ttk import *
import ctypes
import time
from PIL import ImageGrab

bbox = (670, 360, 1860, 1080)  #(1190x720)

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
            print('特殊符号')

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def get_data(yes):
    pth = "C:\\Users\\Limbo\\Desktop\\code\\2024.3\\AI\\lab3\\best.pt"
    model = YOLO(pth)

    bodys=[]
    heads=[]

    while 1:
        if yes.value==0:
            time.sleep(1)
            continue
        if yes.value==1:
            bodys.clear()
            heads.clear()
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
            heads = sorted(heads, key=lambda x: abs((x[0]+x[2])/2+bbox[0]-1280))
            bodys = sorted(bodys, key=lambda x: abs((x[0]+x[2])/2+bbox[0]-1280))
            if len(heads)>=1:
                pydirectinput.moveRel(int((heads[0][0]+heads[0][2])/2+bbox[0]-1280), int((heads[0][1]+heads[0][3])/2+bbox[1]-720), duration=0.02,relative=True)
            elif len(bodys)>=1:
                pydirectinput.moveRel(int((bodys[0][0]+bodys[0][2])/2+bbox[0]-1280), int((bodys[0][1]+bodys[0][3])/2+bbox[1]-720), duration=0.02,relative=True)
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


if __name__ == '__main__':
    with Manager() as manager:
        yes = manager.Value('i', 0)

        Get_key = Process(target=get_key, args=(yes,))
        Get_data= Process(target=get_data, args=(yes,))

        Get_key.start()
        Get_data.start()

        Get_key.join()
        Get_data.join()

