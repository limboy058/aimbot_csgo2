from multiprocessing import Process, Queue
import time,random,os


def consumer(q):
    while True:
        res=q.get()
        if res is None: break #收到结束信号则结束
        #time.sleep(random.randint(1,3))
        print('\033[45m%s 吃 %s\033[0m' %(os.getpid(),res))


def producer(q):
    for i in range(10):
        #time.sleep(random.randint(1,3))
        res='包子%s' %i
        ls=[]
        ls.append(res)
        q.put(ls)
        print('\033[46m%s 生产了 %s\033[0m' %(os.getpid(),res))
    q.put(None) #发送结束信号


if __name__ == '__main__':

    q=Queue()
    #生产者们:即厨师们
    p1=Process(target=producer,args=(q,))

    #消费者们:即吃货们
    c1=Process(target=consumer,args=(q,))

    #开始
    p1.start()
    c1.start()
    print('进程间通信-队列-主进程')