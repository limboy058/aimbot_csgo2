# 第四版（最新release版本）

# 自行收集数据集，进行训练，从而可以做到高识别效率，敌我识别，识别csgo2中的鸡
# 优化并重构代码，
# 提供 更多功能（例如强制锁头、  ）
# 提供 更好效果（距离远时移动快，近则移动慢，加快对齐速度并防止震荡）


from multiprocessing import Process, Array, Value
from ultralytics import YOLO
from pynput import keyboard
from tkinter import *
from tkinter.ttk import *
import ctypes
import time
import cv2
import numpy as np
import mss.tools
import win32api,win32con
from ctypes import windll

# todo:修改这两处为合适大小的，居于屏幕中央的正方形像素数量
bbox = (780, 220, 1780, 1220)
bboxstr='1000x1000+780+220'
# todo:修改为你的屏幕大小
bbox_all=(2560,1440)
bbox_mid=(int(bbox_all[0]/2),int(bbox_all[1]/2))

# 屏幕左上角 到 右下角  （x1, y1 ,x2 ,y2)

# todo: 设置为你的pt的绝对路径
pt_path=r'C:\Users\Limbo\Desktop\code\2024.3\AI\lab3\demo_win_pytorch_normal\best_v8s.pt'




def get_key(yes,k,f,c,d):

    lst1=['均打击  ','仅打击t ','仅打击ct']
    lst2=['不自瞄  ','锁身体  ','锁头    ','强制锁头']
    lst3=['关闭','打开']
    lst4=['关闭','打开']
    def on_press(key):
        try:
            if key.char == 'o':
                if yes.value == 0:
                    print("//-----------------------------------------------------------  ")
                    print('开启,参数为:')
                    print('敌我识别:'+lst1[k.value]+', 自瞄状态:'+lst2[f.value]+', 自动开枪:'+lst3[c.value]+', 绘制方框:'+lst4[d.value])
                    #print("  -----------------------------------------------------------//")

                    yes.value = 1
                elif yes.value == 1:
                    #print("//-----------------------------------------------------------  ")
                    print('关闭,此轮检测信息为:')
                    yes.value = 0
            elif key.char == 'p':
                k.value+=1
                k.value%=3
                print('敌我识别:'+lst1[k.value]+', 自瞄状态:'+lst2[f.value]+', 自动开枪:'+lst3[c.value]+', 绘制方框:'+lst4[d.value])
            elif key.char == '[':
                f.value+=1
                f.value%=4
                print('敌我识别:'+lst1[k.value]+', 自瞄状态:'+lst2[f.value]+', 自动开枪:'+lst3[c.value]+', 绘制方框:'+lst4[d.value])
            elif key.char ==']':
                c.value+=1
                c.value%=2
                print('敌我识别:'+lst1[k.value]+', 自瞄状态:'+lst2[f.value]+', 自动开枪:'+lst3[c.value]+', 绘制方框:'+lst4[d.value])
            elif key.char =='\\':
                d.value+=1
                d.value%=2
                print('敌我识别:'+lst1[k.value]+', 自瞄状态:'+lst2[f.value]+', 自动开枪:'+lst3[c.value]+', 绘制方框:'+lst4[d.value])

                
        except AttributeError:
            _=0

    with keyboard.Listener(on_release=on_press) as listener:
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
        #设置窗口不可点击
        hwnd = windll.user32.GetParent(tk.winfo_id())
        exstyle = windll.user32.GetWindowLongW(hwnd, -20)
        exstyle = exstyle | 0x80000 | 0x20
        windll.user32.SetWindowLongW(hwnd, -20, exstyle)
        
        
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


def get_data(yes, k, f, c,
        ct_heads_cnt, ct_heads, 
        ct_bodys_cnt, ct_bodys, 
        t_heads_cnt, t_heads, 
        t_bodys_cnt, t_bodys, 
        chickens_cnt, chickens):
    
    model = YOLO(pt_path)
    m=mss.mss()
    cnt = 0
    t1 = time.time()
    #sum_time0=0
    sum_time1=0
    sum_time2=0
    sum_time3=0
    print('敌我识别:均打击  , 自瞄状态:不自瞄  , 自动开枪:关闭, 绘制方框:打开')
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
            #begin_time=time.time()
            
            im=m.grab(bbox)
            im=np.array(im)
            im = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)

            # cv2.imshow('c', im)
            # cv2.waitKey(1)
            #im = cv2.resize(im, dsize=(640, 640))?

            results = model.predict(source=im, verbose=False, conf=0.65)
            ttmp=results[0].speed
            sum_time1+=ttmp['preprocess']
            sum_time2+=ttmp['inference']
            sum_time3+=ttmp['postprocess']
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

            if ff==0:
                #sum_time0+=time.time()-begin_time
                continue
            elif ff==1:
                if kk==0 or kk==2:
                    for i in range(ctb):
                        dx_new=(ct_bodys[4*i]+ct_bodys[4*i+2])/2+bbox[0]-bbox_mid[0]
                        dy_new=(ct_bodys[4*i+1]+ct_bodys[4*i+3])/2+bbox[1]-bbox_mid[1]
                        dis=dx_new*dx_new+dy_new*dy_new
                        if dis<d2:
                            dx=dx_new
                            dy=dy_new
                            d2=dis
                if kk==0 or kk==1:
                    for i in range(tb):
                        dx_new=(t_bodys[4*i]+t_bodys[4*i+2])/2+bbox[0]-bbox_mid[0]
                        dy_new=(t_bodys[4*i+1]+t_bodys[4*i+3])/2+bbox[1]-bbox_mid[1]
                        dis=dx_new*dx_new+dy_new*dy_new
                        if dis<d2:
                            dx=dx_new
                            dy=dy_new
                            d2=dis
            elif ff==2:
                if kk==0 or kk==2:
                    for i in range(cth):
                        dx_new=(ct_heads[4*i]+ct_heads[4*i+2])/2+bbox[0]-bbox_mid[0]
                        dy_new=(ct_heads[4*i+1]+ct_heads[4*i+3])/2+bbox[1]-bbox_mid[1]
                        dis=dx_new*dx_new+dy_new*dy_new
                        if dis<d2:
                            dx=dx_new
                            dy=dy_new
                            d2=dis
                if kk==0 or kk==1:
                    for i in range(th):
                        dx_new=(t_heads[4*i]+t_heads[4*i+2])/2+bbox[0]-bbox_mid[0]
                        dy_new=(t_heads[4*i+1]+t_heads[4*i+3])/2+bbox[1]-bbox_mid[1]
                        dis=dx_new*dx_new+dy_new*dy_new
                        if dis<d2:
                            dx=dx_new
                            dy=dy_new
                            d2=dis
            elif ff==3:
                if kk==0 or kk==2:
                    for i in range(cth):
                        dx_new=(ct_heads[4*i]+ct_heads[4*i+2])/2+bbox[0]-bbox_mid[0]
                        dy_new=(ct_heads[4*i+1]+ct_heads[4*i+3])/2+bbox[1]-bbox_mid[1]
                        dis=dx_new*dx_new+dy_new*dy_new
                        if dis<d2:
                            dx=dx_new
                            dy=dy_new
                            d2=dis
                    for i in range(ctb):
                        dx_new=(ct_bodys[4*i]+ct_bodys[4*i+2])/2+bbox[0]-bbox_mid[0]
                        dy_new=(ct_bodys[4*i+1]*11/12+ct_bodys[4*i+3]*1/12)+bbox[1]-bbox_mid[1]
                        dis=dx_new*dx_new+dy_new*dy_new
                        if dis<d2:
                            dx=dx_new
                            dy=dy_new
                            d2=dis
                if kk==0 or kk==1:
                    for i in range(th):
                        dx_new=(t_heads[4*i]+t_heads[4*i+2])/2+bbox[0]-bbox_mid[0]
                        dy_new=(t_heads[4*i+1]+t_heads[4*i+3])/2+bbox[1]-bbox_mid[1]
                        dis=dx_new*dx_new+dy_new*dy_new
                        if dis<d2:
                            dx=dx_new
                            dy=dy_new
                            d2=dis
                    for i in range(tb):
                        dx_new=(t_bodys[4*i]+t_bodys[4*i+2])/2+bbox[0]-bbox_mid[0]
                        dy_new=(t_bodys[4*i+1]*11/12+t_bodys[4*i+3]/12)+bbox[1]-bbox_mid[1]
                        dis=dx_new*dx_new+dy_new*dy_new
                        if dis<d2:
                            dx=dx_new
                            dy=dy_new
                            d2=dis
            #print(d2)
            if d2==100000000:continue#未检测到目标
            if cc==1:
                if ff==1 and d2<100 or (ff==2 or ff==3)and d2<30:
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,bbox_mid[0],bbox_mid[1],0,0)#按下
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,bbox_mid[0],bbox_mid[1],0,0)#抬起
            if d2<40000:
                # Logitech.mouse.move(int(dx), int(dy))
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,int(0.6*dx),int(0.6*dy))
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,int(0.2*dx),int(0.2*dy))
            else:
                # Logitecsah.mouse.move(int(2*dx), int(2*dy))
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,int(1.2*dx),int(1.2*dy))
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,int(0.4*dx),int(0.4*dy))
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,int(0.2*dx),int(0.2*dy))

            #sum_time0+=time.time()-begin_time   
        #yes.value=0
        if yes.value == 0:
            t2 = time.time()
            
            print("计算了%d帧,检算帧率为%f" % (cnt, cnt / (t2 - t1)))
            print("每帧延时(即用时)%fms ,YOLO推理平均耗时%fms" % ((t2 - t1)*1000/cnt,(sum_time1+sum_time2+sum_time3)/cnt))
            #print("预处理耗时%fms,推理耗时%fms,后处理耗时%fms" % (sum_time1/cnt,sum_time2/cnt,sum_time3/cnt))
            print("  -----------------------------------------------------------//")
            sum_time1=0
            sum_time2=0
            sum_time3=0
            cnt=0


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
    d = Value('i', 1, lock=False) # 是否 绘制图像


    

    Get_data = Process(target=get_data, args=(
        yes, k, f, c,
        ct_heads_cnt, ct_heads, 
        ct_bodys_cnt, ct_bodys, 
        t_heads_cnt, t_heads, 
        t_bodys_cnt, t_bodys, 
        chickens_cnt, chickens
    ))

    Get_key = Process(target=get_key, args=(yes, k, f, c, d))


    Draw_screen = Process(target=draw_screen, args=(
        yes, d, 
        ct_heads_cnt, ct_heads, 
        ct_bodys_cnt, ct_bodys, 
        t_heads_cnt, t_heads, 
        t_bodys_cnt, t_bodys, 
        chickens_cnt, chickens
    ))



    Get_key.start()
    Get_data.start()
    Draw_screen.start()


    Get_key.join()
    Get_data.join()
    Draw_screen.join()
