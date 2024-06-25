# 第五版

# 由于持续开枪会使准星在屏幕上上移，且需要时间使弹道恢复，因此尝试优化自动开枪体验
# （未完成）



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
import cv2
import numpy as np
import sys
sys.path.append('C:\\Users\\Limbo\\Desktop\\code\\2024.3\\AI\\lab3\\demo')
import DXGI

import mss.tools
bbox = (780, 220, 1780, 1220)
bboxstr='1000x1000+780+220'
m=mss.mss()

  # 屏幕左上角 到 右下角  （x1, y1 ,x2 ,y2)



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


def get_key(yes,k,f,c,d):

    lst1=['均打击','仅打击t','仅打击ct']
    lst2=['不自瞄','锁身体','锁头','强制锁头']

    def on_press(key):
        try:
            if key.char == 'o':
                if yes.value == 0:
                    print('开启')
                    yes.value = 1
                elif yes.value == 1:
                    print('关闭,此轮检测信息为:')
                    yes.value = 0
            elif key.char == 'p':
                k.value+=1
                k.value%=3
                print('敌我识别状态:'+lst1[k.value])
            elif key.char == '[':
                f.value+=1
                f.value%=4
                print('自瞄状态:'+lst2[f.value])
            elif key.char ==']':
                if c.value==0:
                    print('自动开枪:打开')
                    c.value = 1 
                else:
                    print('自动开枪:关闭')
                    c.value = 0 
            elif key.char =='\\':
                if d.value==0:
                    print('绘制方框:打开')
                    d.value = 1 
                else:
                    print('绘制方框:关闭')
                    d.value = 0 
                
        except AttributeError:
            _=0

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def draw_screen(yes, d, 
        ct_heads_cnt, ct_heads, 
        ct_bodys_cnt, ct_bodys, 
        t_heads_cnt, t_heads, 
        t_bodys_cnt, t_bodys, 
        chickens_cnt, chickens):
    def draw_circle():
        canvas.delete("all")  # 删除先前的所有图案
        canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill=TRANSCOLOUR, outline=TRANSCOLOUR)
        if yes.value==0 or d.value==0:
            time.sleep(1)
            return
        
        for i in range(0,chickens_cnt.value):
            canvas.create_rectangle(chickens[4*i],chickens[4*i+1],chickens[4*i+2],chickens[4*i+3],fill=TRANSCOLOUR,outline='black')

        for i in range(0,t_bodys_cnt.value):
            canvas.create_rectangle(t_bodys[4*i],t_bodys[4*i+1],t_bodys[4*i+2],t_bodys[4*i+3],fill=TRANSCOLOUR,outline='fuchsia')

        for i in range(0,ct_bodys_cnt.value):
            canvas.create_rectangle(ct_bodys[4*i],ct_bodys[4*i+1],ct_bodys[4*i+2],ct_bodys[4*i+3],fill=TRANSCOLOUR,outline='green')
 
        for i in range(0,t_heads_cnt.value):
            canvas.create_rectangle(t_heads[4*i],t_heads[4*i+1],t_heads[4*i+2],t_heads[4*i+3],fill=TRANSCOLOUR,outline='red')
        
        for i in range(0,ct_heads_cnt.value):
            canvas.create_rectangle(ct_heads[4*i],ct_heads[4*i+1],ct_heads[4*i+2],ct_heads[4*i+3],fill=TRANSCOLOUR,outline='blue')
        
        
        
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
    tk.geometry(bboxstr)
    tk.overrideredirect(True)
    tk.wm_attributes('-transparentcolor', TRANSCOLOUR)
    tk.attributes("-topmost",True)
    canvas = Canvas(tk)
    canvas.pack(fill=BOTH, expand=Y)
    update_circle()
    tk.mainloop()


def get_data(yes, k, f, c,tim,
        ct_heads_cnt, ct_heads, 
        ct_bodys_cnt, ct_bodys, 
        t_heads_cnt, t_heads, 
        t_bodys_cnt, t_bodys, 
        chickens_cnt, chickens):
    model = YOLO(r'C:\Users\Limbo\Desktop\code\2024.3\AI\lab3\demo\best.pt')
    g = DXGI.capture(*bbox)
    cnt = 0
    t1 = time.time()
    while(1):
        
        if yes.value == 0:
                time.sleep(1)
                continue
        elif cnt == 0:
            t1 = time.time()
        
        kk=k.value
        ff=f.value
        cc=c.value

        for t in range(50):
            cnt += 1
            #time.sleep(0.01)
            im = g.cap()
            # im=m.grab(bbox)
            # im=np.array(im)
            # im = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)

            # cv2.imshow('c', im)
            # cv2.waitKey(1)
            #im = cv2.resize(im, dsize=(640, 640))?

            results = model.predict(source=im, verbose=False, conf=0.65)
            cth=0 #ct的head的cnt为0 
            ctb=0
            th=0
            tb=0
            chickensc=0
            b = results[0].cpu().boxes
            box = b.xyxy.numpy()
            cls = b.cls.numpy()
            conf =b.conf.numpy()

            for i in range(len(cls)):
                #print(conf[i])
                if cls[i] == 0:
                    ct_heads[cth * 4] = box[i][0] 
                    ct_heads[cth * 4+1] = box[i][1] 
                    ct_heads[cth * 4+2] = box[i][2] 
                    ct_heads[cth * 4+3] = box[i][3] 
                    cth += 1
                elif cls[i]==1:
                    ct_bodys[ctb * 4] = box[i][0] 
                    ct_bodys[ctb * 4+1] = box[i][1] 
                    ct_bodys[ctb * 4+2] = box[i][2] 
                    ct_bodys[ctb * 4+3] = box[i][3] 
                    ctb += 1
                elif cls[i]==2:
                    t_heads[th * 4] = box[i][0] 
                    t_heads[th * 4+1] = box[i][1] 
                    t_heads[th * 4+2] = box[i][2] 
                    t_heads[th * 4+3] = box[i][3] 
                    th += 1
                elif cls[i]==3:
                    t_bodys[tb * 4] = box[i][0] 
                    t_bodys[tb * 4+1] = box[i][1] 
                    t_bodys[tb * 4+2] = box[i][2] 
                    t_bodys[tb * 4+3] = box[i][3] 
                    tb += 1
                else:
                    chickens[chickensc * 4] = box[i][0] 
                    chickens[chickensc * 4+1] = box[i][1] 
                    chickens[chickensc * 4+ 2] = box[i][2] 
                    chickens[chickensc * 4+ 3] = box[i][3] 
                    chickensc += 1

            ct_heads_cnt.value=cth
            ct_bodys_cnt.value=ctb
            t_heads_cnt.value=th
            t_bodys_cnt.value=tb
            chickens_cnt.value=chickensc
            
            dx=0
            dy=0
            d2=100000000 #欧氏距离的平方

            if ff==0:continue
            elif ff==1:
                if kk==0 or kk==2:
                    for i in range(ctb):
                        dx_new=(ct_bodys[4*i]+ct_bodys[4*i+2])/2+bbox[0]-1280
                        dy_new=(ct_bodys[4*i+1]+ct_bodys[4*i+3])/2+bbox[1]-720
                        dis=dx_new*dx_new+dy_new*dy_new
                        if dis<d2:
                            dx=dx_new
                            dy=dy_new
                            d2=dis
                if kk==0 or kk==1:
                    for i in range(tb):
                        dx_new=(t_bodys[4*i]+t_bodys[4*i+2])/2+bbox[0]-1280
                        dy_new=(t_bodys[4*i+1]+t_bodys[4*i+3])/2+bbox[1]-720
                        dis=dx_new*dx_new+dy_new*dy_new
                        if dis<d2:
                            dx=dx_new
                            dy=dy_new
                            d2=dis
            elif ff==2:
                if kk==0 or kk==2:
                    for i in range(cth):
                        dx_new=(ct_heads[4*i]+ct_heads[4*i+2])/2+bbox[0]-1280
                        dy_new=(ct_heads[4*i+1]+ct_heads[4*i+3])/2+bbox[1]-720
                        dis=dx_new*dx_new+dy_new*dy_new
                        if dis<d2:
                            dx=dx_new
                            dy=dy_new
                            d2=dis
                if kk==0 or kk==1:
                    for i in range(th):
                        dx_new=(t_heads[4*i]+t_heads[4*i+2])/2+bbox[0]-1280
                        dy_new=(t_heads[4*i+1]+t_heads[4*i+3])/2+bbox[1]-720
                        dis=dx_new*dx_new+dy_new*dy_new
                        if dis<d2:
                            dx=dx_new
                            dy=dy_new
                            d2=dis
            elif ff==3:
                if kk==0 or kk==2:
                    for i in range(cth):
                        dx_new=(ct_heads[4*i]+ct_heads[4*i+2])/2+bbox[0]-1280
                        dy_new=(ct_heads[4*i+1]+ct_heads[4*i+3])/2+bbox[1]-720
                        dis=dx_new*dx_new+dy_new*dy_new
                        if dis<d2:
                            dx=dx_new
                            dy=dy_new
                            d2=dis
                    for i in range(ctb):
                        dx_new=(ct_bodys[4*i]+ct_bodys[4*i+2])/2+bbox[0]-1280
                        dy_new=(ct_bodys[4*i+1]*11/12+ct_bodys[4*i+3]*1/12)+bbox[1]-720
                        dis=dx_new*dx_new+dy_new*dy_new
                        if dis<d2:
                            dx=dx_new
                            dy=dy_new
                            d2=dis
                if kk==0 or kk==1:
                    for i in range(th):
                        dx_new=(t_heads[4*i]+t_heads[4*i+2])/2+bbox[0]-1280
                        dy_new=(t_heads[4*i+1]+t_heads[4*i+3])/2+bbox[1]-720
                        dis=dx_new*dx_new+dy_new*dy_new
                        if dis<d2:
                            dx=dx_new
                            dy=dy_new
                            d2=dis
                    for i in range(tb):
                        dx_new=(t_bodys[4*i]+t_bodys[4*i+2])/2+bbox[0]-1280
                        dy_new=(t_bodys[4*i+1]*11/12+t_bodys[4*i+3]/12)+bbox[1]-720
                        dis=dx_new*dx_new+dy_new*dy_new
                        if dis<d2:
                            dx=dx_new
                            dy=dy_new
                            d2=dis
            #print(d2)
            if d2==100000000:continue#未检测到目标
            # if cc==1:
            #     if ff==1 and d2<100 or ff==2 and d2<30 and tim.value==0:
            #         Logitech.mouse.press(1)
            #         tim.value=time.time()
            if d2<40000:
                Logitech.mouse.move(int(0.6*dx), int(0.6*dy))
                Logitech.mouse.move(int(0.2*dx), int(0.2*dy))
                Logitech.mouse.move(int(0.1*dx), int(0.1*dy))
            else:
                Logitech.mouse.move(int(1.0*dx), int(1.0*dy))
                Logitech.mouse.move(int(0.3*dx), int(0.3*dy))
                Logitech.mouse.move(int(0.1*dx), int(0.1*dy))
        #yes.value=0
        if yes.value == 0:
            t2 = time.time()
            print("计算了%d帧,检算帧率为%f" % (cnt, cnt / (t2 - t1)))
            cnt=0


def auto_release(tim):
    while(1):
        if tim.value==0 :continue
        if(time.time()-tim.value>1):
            Logitech.mouse.release(1)
            tim.value=0

if __name__ == '__main__':
    ct_heads_cnt = Value('i', 0, lock=False)
    ct_heads = Array('i', 20, lock=False)

    ct_bodys_cnt = Value('i', 0, lock=False)
    ct_bodys = Array('i', 20, lock=False)

    t_heads_cnt = Value('i', 0, lock=False)
    t_heads = Array('i', 20, lock=False)

    t_bodys_cnt = Value('i', 0, lock=False)
    t_bodys = Array('i', 20, lock=False)

    chickens_cnt= Value('i', 0, lock=False)
    chickens = Array('i', 20, lock=False)

    yes = Value('i', 0, lock=False) #是否开启功能
    k = Value('i', 0, lock=False) # 敌我识别,0表示均打,1表示打击t,2表示打击ct
    f = Value('i', 0, lock=False) #功能,0表示不自瞄,1表示锁身体,2表示锁头,3表示强制锁头(如果找不到头,根据身体计算头部位置)
    c = Value('i', 0, lock=False) #是否 自动开枪
    d = Value('i', 1, lock=False) # 是否绘制图像
    tim =Value('d', 0, lock=False) # 按下开枪的时间戳

    Get_key = Process(target=get_key, args=(yes, k, f, c, d))

    Get_data = Process(target=get_data, args=(
        yes, k, f, c, tim,
        ct_heads_cnt, ct_heads, 
        ct_bodys_cnt, ct_bodys, 
        t_heads_cnt, t_heads, 
        t_bodys_cnt, t_bodys, 
        chickens_cnt, chickens
    ))

    Draw_screen = Process(target=draw_screen, args=(
        yes, d, 
        ct_heads_cnt, ct_heads, 
        ct_bodys_cnt, ct_bodys, 
        t_heads_cnt, t_heads, 
        t_bodys_cnt, t_bodys, 
        chickens_cnt, chickens
    ))

    #Auto_re=Process(target=auto_release,args=(tim,))

    Get_key.start()
    Get_data.start()
    Draw_screen.start()
    #Auto_re.start()

    Get_key.join()
    Get_data.join()
    Draw_screen.join()
    #Auto_re.join()
