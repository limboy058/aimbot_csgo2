
import sys
import win32api
import os # 获取文件路径
import time # 获取时间和延时
import ctypes # 调用dll文件

import tkinter as tk # python 内置库,需要安装时勾选安装IDE才会安装,坑爹
import threading # 多线程
import pyautogui # 获取屏幕鼠标坐标
import random # 随机数


class PID:
    """PID"""
    def __init__(self, P=0.35, I=0, D=0):
        """PID"""
        self.kp = P # 比例 
        self.ki = I # 积分
        self.kd = D # 微分
        self.uPrevious = 0 # 上一次控制量
        self.uCurent = 0 # 这一次控制量
        self.setValue = 0 # 目标值
        self.lastErr = 0 # 上一次差值
        self.errSum = 0 # 所有差值的累加
        self.errSumLimit = 10 # 近两次的差值累加
        
    def pidPosition(self, setValue, curValue):
        """位置式 PID 输出控制量"""
        self.setValue = setValue # 更新目标值
        err = self.setValue - curValue # 计算差值, 作为比例项
        dErr = err - self.lastErr # 计算近两次的差值, 作为微分项
        self.errSum += err # 累加这一次差值,作为积分项
        outPID = (self.kp * err) + (self.ki * self.errSum) + (self.kd * dErr) # PID
        self.lastErr = err # 保存这一次差值,作为下一次的上一次差值
        return outPID # 输出
    
    def pidIncrease(self, setValue, curValue):
        """增量式 PID 输出控制量的差值"""
        self.uCurent = self.pidPosition(setValue, curValue) # 计算位置式
        outPID = self.uCurent - self.uPrevious # 计算差值 
        self.uPrevious = self.uCurent # 保存这一次输出量
        return outPID # 输出

class LOGITECH:
    """罗技动态链接库"""
    try:
        file_path = os.path.abspath(os.path.dirname(__file__)) # 当前路径
        dll = ctypes.CDLL(f'{file_path}/logitechdriver.dll') # 打开路径文件
        state = (dll.device_open() == 1) # 启动, 并返回是否成功
        WAIT_TIME = 0.5 # 等待时间
        RANDOM_NUM = 0.1 # 最大时间随机数
        if not state:
            print('错误, 未找到GHUB或LGS驱动程序')
    except FileNotFoundError:
        print(f'错误, 找不到DLL文件')

    def __init__(self) -> None:
        pass

    @classmethod
    def mouse_move(self, end_xy, wait_time=0, min_xy=2, min_time=0.1):
        """
        等待多久后 缓慢移动 \n
        end_x       绝对横坐标 \n
        end_y       绝对纵坐标 \n
        time_s      等待时间 \n
        min_xy      最小移动控制量 \n
        min_time    最小移动时间 \n
        """
        if wait_time == 0: # 如果没有规定等待时间
            wait_time = self.WAIT_TIME # 默认等待时间
        if wait_time != 0: # 如果等待时间不是0
            wait_time += random.uniform(0, self.RANDOM_NUM)
            time.sleep(wait_time) # 延时时间,秒,生成随机小数0~1.0
        if not self.state: # 保护措施
            return
        
        end_x, end_y = end_xy
        print_tkui(f'等待{wait_time:.2f}秒后, 移动到坐标{(end_x, end_y)}')

        pid_x = PID() # 创建pid对象
        pid_y = PID()

        while True: # 循环控制鼠标直到重合坐标
            #time.sleep(min_time) # 延时时间,秒,生成随机小数0~1.0
            new_x, new_y = pyautogui.position() # 获取当前鼠标位置

            move_x = pid_x.pidPosition(end_x, new_x) # 经过pid计算鼠标运动量
            move_y = pid_y.pidPosition(end_y, new_y)

            print(f'x={new_x}, y={new_y}, xd={move_x}, yd={move_y}')
            if end_x == new_x and end_y == new_y: # 如果重合就退出循环
                break
            
            if move_x > 0 and move_x < (min_xy): # 限制正最小值
                move_x = (min_xy)
            elif move_x < 0 and move_x > -(min_xy): # 限制负最小值
                move_x = -(min_xy)
            else:
                move_x = int(move_x) # 需要输入整数,小数会报错

            if move_y > 0 and move_y < (min_xy):
                move_y = (min_xy)
            elif move_y < 0 and move_y > -(min_xy):
                move_y = -(min_xy)
            else:
                move_y = int(move_y)

            self.dll.moveR(move_x, move_y, False) # 貌似有第三个参数,但是没试出来什么用

    @classmethod
    def mouse_down(self, code):
        """ 鼠标按下 code: 左 中 右 """
        if not self.state:
            return
        print_tkui(f'按下{code}键')
        if code == '左':
            code = 1
        elif code == '中':
            code = 2
        elif code == '右':
            code = 3
        else: # 默认
            code = 1 
        self.dll.mouse_down(code)

    @classmethod
    def mouse_up(self, code):
        """ 鼠标松开 code: 左 中 右 """
        if not self.state:
            return
        print_tkui(f'松开{code}键')
        if code == '左':
            code = 1
        elif code == '中':
            code = 2
        elif code == '右':
            code = 3
        else: # 默认
            code = 1 
        self.dll.mouse_up(code)
    
    @classmethod
    def mouse_click(self, code, wait_time=0):
        """ 鼠标点击 code: 左 中 右 """
        if wait_time == 0: # 如果没有规定等待时间
            wait_time = self.WAIT_TIME # 默认等待时间
        if wait_time != 0: # 如果等待时间不是0
            wait_time += random.uniform(0, self.RANDOM_NUM)
            time.sleep(wait_time) # 延时时间,秒,生成随机小数0~1.0
            
        if not self.state:
            return
        print_tkui(f'等待{wait_time:.2f}秒后, 点击{code}键')
        if code == '左':
            code = 1
        elif code == '中':
            code = 2
        elif code == '右':
            code = 3
        else: # 默认
            code = 1 

        self.dll.mouse_down(code)
        time.sleep(random.uniform(0, self.RANDOM_NUM)) # 延时时间,秒,生成随机小数0~1.0
        self.dll.mouse_up(code)


def print_tkui(strs):
    """ 打包控制台输出 """
    print(strs)


if __name__=='__main__':
    LOGITECH.mouse_move((200,200))