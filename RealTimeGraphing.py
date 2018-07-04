from collections import deque
import tkinter as tk               # import Tkinter module (class)
from tkinter import font as tkfont # from  Tkinter module (class) import 'font' class
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from tkinter import ttk #import ttk class from tkinter nodule. Tkk is a themed widged that inherits from widget
import time
import csv
from threading import Thread
import multiprocessing
from multiprocessing import Process
from tkinter import messagebox
import serial
import timeit

#no tkinter!!
class staticVariables(object):
    currentReading=0

def recordValues():
    #countdown = 500
    i = 1
    a = 18119   #last x value
    b = 1.9
    while (countdown != 0):
        time.sleep(1);
        #print(str(i))
        i = i + 1
        with open('1153_testV2csv.csv', 'a', newline='') as csvfile:     #'a' for appending, 'w' for overriding (erase all then write) and 'r' for readonly
            fieldnames = ['x', 'y']   #x and y headers
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames) # DictWriter does same thing as a writerclass
            #writer.writeheader()    #add column titles
            writer.writerow({'x': str(a), 'y': str(b)})
            a = a + 100
            if i % 2 > 0:
                b = 1.915
            else:
                b = 1.885
            staticVariables.currentReading = b         
            --countdown

class subGraphingRoutine(tk.Frame):
    print("sub graph")
    def __init__(self, parent):
        print("subgraphing routine")
        tk.Frame.__init__(self, parent)
        style.use('fivethirtyeight')
        #label = ttk.Label(self,text="Extrusion Line: Dynamic Grapher", font=staticVariables.title_font).pack() #tkk extends tkinter widget. Create label object.
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(fill = tk.BOTH, expand=1)
        toolbar = NavigationToolbar2TkAgg(canvas, self )
        toolbar.update()

class currentReading(tk.Label):
    def __init__(self,parent):
        tk.Label.__init__(self,parent, text = staticVariables.currentReading, font = ("Courier", 20))
        #self.text="hello"                   #Operator
        self.pack()

        def getCurrent():
            self.config(text = staticVariables.currentReading)
            print("hellooo")
            self.after(500,getCurrent)
        getCurrent()

   
class FixedInterval(tk.Tk):  #DynamicPage inherits from Frame class. DynamicPage 'is a' Frame
    def __init__(self): #override the frame cosntructor
        print("fixed interval init")
        tk.Tk.__init__(self)     # child must explicitly call parent constructor. 'Frame' is the parent class.   

        label = tk.Label(self, text="Last X minutes")   #create label object
        label.pack()
        frame = tk.Frame(self)
        frame.pack(fill=tk.X)
        filler = tk.Frame(frame) 
        filler.pack(side=tk.LEFT, fill = tk.X, expand = 1)              
        group = ttk.LabelFrame(frame, text="Current Reading")   #frame containing main parameters
        group.pack(side=tk.LEFT,fill = tk.X)
        lbl = currentReading(group)
        #lbl=tk.Label(group, text = "Hello")
        #lbl.pack()

        self.state = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        self.geometry('900x900+200+200')
        fixedGraph = subGraphingRoutine(self)
        fixedGraph.pack(fill=tk.BOTH, expand = 1)
        #self.attributes("-fullscreen", True)
            
    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)
        return "break"    

def animate(j):
    #print("animation being called!")
    graph_data = open('1153_testV2csv.csv','r').read()  #open samplefile with the intention to read
    lines = graph_data.split('\n')
    #primary series
    xs = [] #x-axis collection shared among all series
    ys = [] #y-axis collection
    #secondary series
    ucl = []
    lcl = []
    #create secondary series

       
    #create primary series
    for line in lines:   
        if len(line)>1: #check that line isnt't totally empty
            x,y = line.split(',')
            xs.append(x)    #attach/insert new list onto the x-axis collection
            ys.append(y)    #attach/insert new list onto the y-axis collection
            ucl.append(1.915) 
            lcl.append(1.885)
    ax1.clear()
    ax1.plot(xs, ys)
    #ax1.setp(lines, linewidth=1)   
    ax1.plot(xs, ucl,linewidth=1, label='UCL', color='r')  
    ax1.plot(xs, lcl, label='LCL', color='r')
    ax1.legend(bbox_to_anchor=(1.00, 1), loc=2, borderaxespad=0.)

 

#def aniFunc():            
#    fig = plt.figure()
#    ax1 = fig.add_subplot(1,1,1)    # subplot on a grid system
#    ani = animation.FuncAnimation(fig, animate, interval = 1000)       #alows you to animate based on a fucntion,'fig' = where to animate function to, 'animate' - function that we're going to animate, 'interval' = rate
#    plt.show()

if __name__ == '__main__':
        global countdown
        countdown = 500
        Thread(target = recordValues).start()
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        app = FixedInterval()
        ani = animation.FuncAnimation(fig, animate, interval = 1000)       #alows you to animate based on a fucntion,'fig' = where to animate function to, 'animate' - function that we're going to animate, 'interval' = rate
        tk.mainloop()

        
