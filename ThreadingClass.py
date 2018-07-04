import time
from threading import Thread

#Thread(target = recordValues).start()

class App(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()

    def run(self):
        i = 0
        while True:
            print(i)
            i = i + 1
            time.sleep(1)

testObj = App()
while True:
    print("hello jason")
    time.sleep(2)
