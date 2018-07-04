#from Tkinter import *
from collections import deque
import tkinter as tk               # import Tkinter module (class)
from tkinter import font as tkfont # from  Tkinter module (class) import 'font' class
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkinter as Tk
from tkinter import ttk #import ttk class from tkinter nodule. Tkk is a themed widged that inherits from widget
import time
import csv
from threading import Thread
import multiprocessing
from multiprocessing import Process
import os
import pygubu
#from Tkinter import *
#pygubu-designer.exe

class staticVariables(object):
    fig = plt.figure()             #variables outside functions are equivalent to static variables     
    ax1 = fig.add_subplot(1,1,1)
    title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

#class 4.5FstaticVariables(object):
#    fig = plt.figure()             #variables outside functions are equivalent to static variables     
#    ax1 = fig.add_subplot(1,1,1)        
    
class subGraphingRoutine(tk.Frame): 
    def __init__(self, parent):  
        tk.Frame.__init__(self, parent)
        style.use('fivethirtyeight')
        label = ttk.Label(self,text="Extrusion Line: Dynamic Grapher").pack() #tkk extends tkinter widget. Create label object.
        canvas = FigureCanvasTkAgg(staticVariables.fig, master=self)
        canvas.get_tk_widget().pack()
        toolbar = NavigationToolbar2TkAgg(canvas, self )
        toolbar.update()

class MainGUI(tk.Tk):
    def __init__(self):  
        tk.Tk.__init__(self)        #create main frame
        #1: Create a builder
        self.builder = builder = pygubu.Builder()
        #2: Load a ui file
        builder.add_from_file('MainGUI.ui')
        #3: Create the widget using self as parent
        self.mainwindow = builder.get_object('mainwindow',self)  #main window is a frame object
        #print(str(cbooo))
        #4: Connect callbacks
        builder.connect_callbacks(self)
        #display message

    def testCommand(self):
            builder = pygubu.Builder()
            builder.add_from_file('MainGUI.ui')
            cbooo = builder.get_object('cboCableType','mainwindow')  #main window is a frame object 
            #print(str(cbooo))

    def showGraph():       #not an instance method, purely a do something methd. Instance methods are inline with the constructor and take self as a default parameter.
        quit()              #destroys reference to object but object still exists.    
        app = FixedInterval()
        root = app
        aniObj = Animate(180, 1.915, 1.885, 0, 0)
        ani = animation.FuncAnimation(staticVariables.fig, aniObj.animate, interval = 1000)
        tk.mainloop()



    def quit():
        self.destroy()

class LoginPage(tk.Tk):
    def __init__(self):        
        tk.Tk.__init__(self)
        def showGraph1():       #not an instance method, purely a do something methd. Instance methods are inline with the constructor and take self as a default parameter.
            quit()              #destroys reference to object but object still exists.    
            app = FixedInterval()
            root = app
            aniObj = Animate(180, 1.915, 1.885, 0, 0)
            ani = animation.FuncAnimation(staticVariables.fig, aniObj.animate, interval = 1000)
            tk.mainloop()
        
        def quit():
            self.destroy()
        
        lblLot = tk.Label(self, text="Label", font = staticVariables.title_font) 
        lblLot.pack()
        btnGo = tk.Button(self, text="Go", command=showGraph1)  #lambda allows you to reference functions which require arguments (in buttons)     
        btnGo.pack()
        btnQuit = tk.Button(self, text="Quit", command=quit)  #lambda allows you to reference functions which require arguments (in buttons)     
        btnQuit.pack()

class FixedInterval(tk.Tk):  #DynamicPage inherits from Frame class. DynamicPage 'is a' Frame
    def __init__(self): #override the frame cosntructor
        tk.Tk.__init__(self)     # child must explicitly call parent constructor. 'Frame' is the parent class.
        def quit():
            #ThreadObject()
            app = EntireGraph()
            self.destroy()
            aniObj = AnimateEntireGraph(1.519, 1.485, 0, 0)
            ani = animation.FuncAnimation(staticVariables.fig, aniObj.animate, interval = 1000)
            tk.mainloop()

        def center(toplevel):
            toplevel.update_idletasks()
            w = toplevel.winfo_screenwidth()
            h = toplevel.winfo_screenheight()
            size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
            x = w/2 - size[0]/2
            y = h/2 - size[1]/2
            toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

        label = tk.Label(self, text="Last X minutes", font=staticVariables.title_font)   #create label object
        label.pack(side="top", fill="x", pady=10)
        fixedGraph = subGraphingRoutine(self)
        fixedGraph.pack()
        btnShow = tk.Button(self, text="Show entire graph", command=quit)  #lambda allows you to reference functions which require arguments (in buttons)     
        btnShow.pack()  #button is organized into a blocks similar to HTML
        #win = tk.Toplevel(self)
        #win.title("Centered!")
        center(self)


class ThreadObject(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()

    def run(self):
        import EntireGraph

class EntireGraph(tk.Tk):        
    def __init__(self): #override the frame cosntructor
        tk.Tk.__init__(self)     # child must explicitly call parent constructor. 'Frame' is the parent class.
        def quit():
            app = FixedInterval()
            self.destroy()
            aniObj = Animate(180, 1.915, 1.885, 0, 0)
            ani = animation.FuncAnimation(staticVariables.fig, aniObj.animate, interval = 1000)
            tk.mainloop()

        def center(toplevel):
            toplevel.update_idletasks()
            w = toplevel.winfo_screenwidth()
            h = toplevel.winfo_screenheight()
            size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
            x = w/2 - size[0]/2
            y = h/2 - size[1]/2
            toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

        label = tk.Label(self, text="Entire Graph", font=staticVariables.title_font)   #create label object
        label.pack(side="top", fill="x", pady=10)
        entireGraph = subGraphingRoutine(self)
        entireGraph.pack()
        btnShow = tk.Button(self, text="Show Fixed graph", command=quit)  #lambda allows you to reference functions which require arguments (in buttons)     
        btnShow.pack()  #button is organized into a blocks similar to HTML           
        center(self)
              
class Animate(object):    #animate 6F object
    def __init__(self, xInterval, ucl, lcl, usl, lsl):  
        global xInterval_val, ucl_val, lcl_val, usl_val, lsl_val
        xInterval_val = xInterval
        ucl_val = ucl
        lcl_val = lcl
        usl_val = usl
        lsl_val = lsl
    
    @classmethod
    def alternateConstructor(cls, ucl, lcl, usl, lsl):
        ucl_val = ucl
        lcl_val = lcl
        usl_val = usl
        lsl_val = lsl
        return cls(None, ucl_val, lcl_val, usl_val, lsl_val)

    def animate(self, i): #i for 'interval'
        #print(str(nigga))
        graph_data = open('1153_testcsv.csv','r').read()  #open samplefile with the intention to read
        lines = graph_data.split('\n')
        ys = deque(maxlen=xInterval_val) #y-axis collection
        xs = deque(maxlen=xInterval_val)
        ucl = deque(maxlen=xInterval_val)
        lcl = deque(maxlen=xInterval_val)
        for line in lines:   
            if len(line)>1: #check that line isnt't totally empty
                x,y = line.split(',')
                xs.append(x)    #attach/insert new list onto the x-axis collection
                ys.append(y)    #attach/insert new list onto the y-axis collection
                ucl.append(ucl_val) 
                lcl.append(lcl_val)
        staticVariables.ax1.clear()
        staticVariables.ax1.plot(xs, ys)
        staticVariables.ax1.plot(xs, ucl, label='UCL', color='r')  
        staticVariables.ax1.plot(xs, lcl, label='LCL', color='r')

class AnimateEntireGraph(Animate):    #animate 6F object
    def __init__(self, ucl, lcl, usl, lsl):  
        Animate.alternateConstructor(ucl, lcl, usl, lsl)

    def animate(self, j): #i for 'interval'
        graph_data = open('1153_testcsv.csv','r').read()  #open samplefile with the intention to read
        lines = graph_data.split('\n')
        ys = []
        xs = []
        ucl = []
        lcl = []
        for line in lines:   
            if len(line)>1: #check that line isnt't totally empty
                x,y = line.split(',')
                xs.append(x)    #attach/insert new list onto the x-axis collection
                ys.append(y)    #attach/insert new list onto the y-axis collection
                ucl.append(ucl_val) 
                lcl.append(lcl_val)
        staticVariables.ax1.clear()
        staticVariables.ax1.plot(xs, ys)
        staticVariables.ax1.plot(xs, ucl, label='UCL', color='r')  
        staticVariables.ax1.plot(xs, lcl, label='LCL', color='r')    


def recordValues():
    i = 0
    a = 18119   #last x value
    b = 1.9
    while (i >= 0):
        time.sleep(1);
        print(str(i))
        i = i + 1
        with open('1153_testcsv.csv', 'a', newline='') as csvfile:     #'a' for appending, 'w' for overriding (erase all then write) and 'r' for readonly
            fieldnames = ['x', 'y']   #x and y headers
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames) # DictWriter does same thing as a writerclass
            #writer.writeheader()    #add column titles
            writer.writerow({'x': str(a), 'y': str(b)})
            a = a + 100
            if i % 2 > 0:
                b = 1.915
            else:
                b = 1.885

   
if __name__ == "__main__":
    #Thread(target = recordValues).start()
    app = MainGUI()
    tk.mainloop()

    

          
