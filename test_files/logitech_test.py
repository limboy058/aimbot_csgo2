import ctypes
import os
import pynput
import winsound

try:
    root = os.path.abspath(os.path.dirname(__file__))
    driver = ctypes.CDLL(r'C:\Users\Limbo\Desktop\code\2024.3\AI\lab3\demo_win_pytorch_normal\logitech_driver.dll')
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
if __name__ == '__main__':  # 测试

    import pyautogui
    Logitech.mouse.move(100, 100)
    while(1):
        t=pyautogui.position()
        print(t,(t.x-1280)*(t.x-1280)+(t.y-720)*(t.y-720))  
    
