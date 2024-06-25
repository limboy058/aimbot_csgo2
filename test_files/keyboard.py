from pynput import keyboard
yes=0

def on_press(key):
    try:
        global yes
        if key.char==']' and yes==0:
            print('开启外挂')
            yes=1
        elif key.char==']' and yes==1:
            print('关闭外挂')
            yes=0
    
        print(f'按键 {key.char} 被按下')
    except AttributeError:
        print(f'特殊按键 {key} 被按下')

def on_release(key):
    print(f'按键 {key} 被释放')
    if key == keyboard.Key.esc:
        # 停止监听
        return False

# 设置监听器
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()