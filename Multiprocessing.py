from multiprocessing import Process, Queue, Pipe
import random
import psutil
import os, signal
from threading import Thread
import psutil

#append a queue each time function runs
class Worker(object):
    def rand_num(queue,conn):
        x = 0
        while True:
            #conn.send([42, None, 'hello'])
            #conn.send(x)
            #pid = os.getpid()
            x = x + 1
            queue.put(x)
        

def startProcess():
    proc = Process(target=Worker.rand_num, args=(queue,child_conn))
    proc.start()
    while True:
        q = queue.get()   
        print(sqtr(q)) 

    #proc.join()

if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    queue = Queue()
    Thread(target=startProcess).start()
    #q = queue.get()
    #while True:
    #    qpipe = parent_conn.recv()
    #    #print(q)
    #    print(str(qpipe))

    #for x in range(0,5):
    #    print(x)
    #print('killing')
    #p = psutil.Process(pidx)
    #p.terminate()
    #os.kill(pid, signal.SIGKILL)
         

    
    #each process has a unique queue
    #grab each queue from each process
    #for p in processes:
   
