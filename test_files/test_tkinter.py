from tkinter import *
from tkinter.ttk import *
import ctypes

def draw_circle():
    canvas.delete("all")  # 删除先前的所有图案
    canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), fill=TRANSCOLOUR, outline=TRANSCOLOUR)

    canvas.create_rectangle(100,30,300,40,fill=TRANSCOLOUR,outline='red')
    canvas.create_rectangle(200,200,220,250,fill=TRANSCOLOUR,outline='red',tag="red")

def update_circle():
    draw_circle()
    tk.after(100, update_circle)


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

