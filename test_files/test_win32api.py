import win32gui, win32ui, win32api, win32con
from win32api import GetSystemMetrics

dc = win32gui.GetDC(0)
dcObj = win32ui.CreateDCFromHandle(dc)
hwnd = win32gui.WindowFromPoint((0,0))
monitor = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))

red = win32api.RGB(255, 0, 0) # Red
past_coordinates = monitor

def draw(x1,y1,x2,y2):
    past_coordinates = (x1, y1, x2, y2)
    rect = win32gui.CreateRoundRectRgn(*past_coordinates, 2 , 2)
    win32gui.RedrawWindow(hwnd, past_coordinates, rect, win32con.RDW_INVALIDATE)

    for x in range(x1,x2):
        win32gui.SetPixel(dc, x, y1, red)
        win32gui.SetPixel(dc, x, y2, red)
    for y in range(y1,y2):
        win32gui.SetPixel(dc, x1, y, red)
        win32gui.SetPixel(dc, x2, y, red)

while True:
    draw(100,200,300,400)
    draw(800,800,1000,1200)