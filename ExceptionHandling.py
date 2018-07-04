x = 5
from tkinter import messagebox

class parameterException(Exception):
    def __init__(self,msg):
        Exception.__init__(self, msg)
        #self.message = msg
    
    #def __str__(self):
    #    return str(self.message)

def check(num):
    if num > 7:
        raise parameterException('value error niggaaaaa')   #throw an error of type parameterException. Error must be thrown from try block.

def doSomething():
    try:
        check(8)    
        print('no error detected')
    except parameterException as pe:      #catch error of type parameterException
        #print(pe)                         #print the string representation of the parameterException object
        messagebox.showerror("Error", pe)

if __name__ == "__main__":
    doSomething()
         