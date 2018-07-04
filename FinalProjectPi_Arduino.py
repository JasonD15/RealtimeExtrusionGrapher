#from Tkinter import *
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
from multiprocessing import Process, Queue, Pipe
from tkinter import messagebox
import serial
import timeit
import shutil
import psutil
import os
from subprocess import call

#change to
#Zumbach - 'g210\r\n'
#Zumbach - ('/dev/ttyUSB0',19200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE, timeout=5)
#Arduino - ('/dev/ttyACM0', 9600, timeout=5)

#Zumbach - ('/dev/ttyUSB0',19200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONtikmE, timeout=5)
#Arduino - ('/dev/ttyACM0', 9600, timeout=5)

#Arduino - ('COM6', 9600, timeout=5)
#Arduino - ('COM4', 9600, timeout=5)
#Arduino - ('COM3', 9600, timeout=5)

#Arduino - 'g210'

#Pi - '/home/pi/Desktop/DynamicGrapher'
#Pi - '/home/pi/Desktop/DynamicGrapher/TestFolder'

#src_path = 'C:/Users/Admin/Dropbox/Python/DynamicGraphing/csvFolder'
#dest_path = 'C:/Users/Admin/Dropbox/Python/DynamicGraphing/RdriveFolder'

#src_path = 'C:/Users/jason.dichoso/Dropbox/Python/DynamicGraphing/csvFolder'
#dest_path = 'C:/Users/jason.dichoso/Dropbox/Python/DynamicGraphing/RdriveFolder'


#src_path = '/home/pi/Desktop/DynamicGrapher/CSV_Files'
#dest_path = '/home/pi/R/Quality/DHR/Cable Making/Real-time Extrusion Grapher'

class parameterException(Exception):
    def __init__(self,msg):
        Exception.__init__(self, msg)

class staticVariables(object):
    fig = plt.figure()             #variables outside functions are equivalent to static variables     
    ax1 = fig.add_subplot(1,1,1)
    bigText = ("Arial", 20, 'bold')
    dropdown_font = ("Times", "16", "bold italic")
    btnfont = ('Sans','20','bold')
    #6F      UCL = 1.470, LCL = 1.400
    #4.5F    UCL = 1.115, LCL = 1.085
    UCL=0
    LCL=0
    operator=''
    cableType=''
    lotNo=''
    csvFileName=''
    mostRecent_xvalue = 0
    isPaused = False
    connectionError = False
    permissionError = False
    readySwitch = False
    aniObj = None
    OnGraphPage = False     
    loginCounter = 0
    closeApp = False
    currentYReading=0    #used for displaying current reading label on graph
    currentXReading=0   #used for annotating the current time value
    localPath=''    #targets generated csv file
    serverPath=''
    isStopped = False
    queue = None
    parent = None
    child = None
    error = None
    pid = 0
    src_path = '/home/pi/Desktop/DynamicGrapher/CSV_Files'  #targets folder containing all csv files
    dest_path = '/home/pi/R/Quality/DHR/Cable Making/Real-time Extrusion Grapher'
    tracker = 1

def setPath():
    staticVariables.localPath = '%s/%s_%s.csv' %(staticVariables.src_path, staticVariables.lotNo,staticVariables.operator)
    staticVariables.serverPath = '%s/%s_%s.csv' %(staticVariables.dest_path, staticVariables.lotNo,staticVariables.operator)

def copyFile():
    #call("sudo mount -a", shell=True)
    src_path = staticVariables.src_path
    dest_path = staticVariables.dest_path
    ls_dir = os.listdir(src_path)   
    i = 0
    for file in ls_dir:
        src = src_path + '/' + str(ls_dir[i])
        dest = dest_path + '/' + str(ls_dir[i])
        i = i + 1
        shutil.copyfile(src, dest)

    
class subGraphingRoutine(tk.Frame): 
    def __init__(self, parent):  
        tk.Frame.__init__(self, parent)
        style.use('fivethirtyeight')
        label = ttk.Label(self,text="Real-time Extrusion Grapher", font=staticVariables.bigText).pack() #tkk extends tkinter widget. Create label object.
        canvas = FigureCanvasTkAgg(staticVariables.fig, master=self)
        canvas.get_tk_widget().pack(fill=tk.BOTH,expand=1)
        toolbar = NavigationToolbar2TkAgg(canvas, self )
        toolbar.update()

def StartNewProcess():
    threadObj = SerialCommunication()

class LoginPage(tk.Tk):
    def __init__(self):      
        tk.Tk.__init__(self)
        def showGraph1():       #not an instance method, purely a do something methd. Instance methods are inline with the constructor and take self as a default parameter.
            try:
                staticVariables.connectionError = False     #refresh booleans
                staticVariables.permissionError = False
                staticVariables.isPaused = False
                staticVariables.isStopped = False

                if len(entry1.get())==0 or len(entry2.get())==0:
                    raise parameterException('Please fill in all fields')
                getDataFields()
                conn = checkConnection()
                if conn == False:
                    raise serial.SerialException
                checkFile()
                staticVariables.readySwitch = True
                Thread(target = StartNewProcess).start()
                print('about to enter while loop')
                while True:
                    if staticVariables.connectionError == True:
                        print("connectionError is true")
                        break
                    elif staticVariables.permissionError == True:
                        messagebox.showerror("Error", "Check .csv file!")
                        break
                    #on login page and no connection error
                    elif (staticVariables.connectionError == False and staticVariables.permissionError == False and staticVariables.readySwitch == True):
                        print("No errors detected")
                        self.destroy()              #destroys reference to object but object still exists.
                        app = FixedInterval()
                        #root = app
                        staticVariables.aniObj = Animate(1200, staticVariables.UCL, staticVariables.LCL, 0, 0)
                        ani = animation.FuncAnimation(staticVariables.fig, staticVariables.aniObj.animate, interval = 1000)
                        break
                    print('while loop enganged')       
                staticVariables.connectionError = False     #refresh booleans
                tk.mainloop()         
            except parameterException as pe:
                messagebox.showerror("Error", pe)
            except serial.SerialException:
                messagebox.showerror("Error", "Check Zumbach connection!")
                return

                            
        def quit():
            btnQuit.config(state = tk.DISABLED)
            self.result = messagebox.askyesno('Are you sure?', 'Quitting will cause the system to shut down.')
            if self.result == True:
                call("sudo nohup shutdown -h now", shell=True)
            else:
                btnQuit.config(state = 'normal')     

        
        def getValue(event):
            global cboValue
            cboValue = cbo.get()
             
        def getDataFields():
            try:                                    #cboValue not yet defined at this stage
                if cboValue == "4.5F Inner Jacket":
                    staticVariables.LCL = 1.085
                    staticVariables.UCL = 1.115
                    staticVariables.operator = entry1.get()
                    staticVariables.lotNo = entry2.get()
                    staticVariables.cableType = '4.5F Inner Jacket'
                    staticVariables.csvFileName = staticVariables.lotNo
                    #print('4.5F inner selected')
                elif cboValue == "6F Inner Jacket":
                    staticVariables.LCL = 1.450
                    staticVariables.UCL = 1.420
                    staticVariables.operator = entry1.get()
                    staticVariables.lotNo = entry2.get()
                    staticVariables.cableType = '6F Inner Jacket'
                    staticVariables.csvFileName = staticVariables.lotNo
                    #print('6F inner selected')
                elif cboValue == "7.5F Inner Jacket":
                    staticVariables.LCL = 1.955
                    staticVariables.UCL = 1.985
                    staticVariables.operator = entry1.get()
                    staticVariables.lotNo = entry2.get()
                    staticVariables.cableType = '7.5F Inner Jacket'
                    staticVariables.csvFileName = staticVariables.lotNo
                    #print('7.5F inner selected')
                elif cboValue == "4.5F Outer Jacket":
                    staticVariables.LCL = 1.504
                    staticVariables.UCL = 1.534
                    staticVariables.operator = entry1.get()
                    staticVariables.lotNo = entry2.get()
                    staticVariables.cableType = '4.5F Outer Jacket'
                    staticVariables.csvFileName = staticVariables.lotNo
                elif cboValue == "6F Outer Jacket":
                    staticVariables.LCL = 1.885
                    staticVariables.UCL = 1.915
                    staticVariables.operator = entry1.get()
                    staticVariables.lotNo = entry2.get()
                    staticVariables.cableType = '6F Outer Jacket'
                    staticVariables.csvFileName = staticVariables.lotNo
                elif cboValue == "7.5F Outer Jacket":
                    staticVariables.LCL = 2.560
                    staticVariables.UCL = 2.520
                    staticVariables.operator = entry1.get()
                    staticVariables.lotNo = entry2.get()
                    staticVariables.cableType = '7.5F Outer Jacket'
                    staticVariables.csvFileName = staticVariables.lotNo
                else:
                    pass
                setPath()
            except:                                #do this by degfault
                staticVariables.LCL = 1.400
                staticVariables.UCL = 1.470
                staticVariables.operator = entry1.get()
                staticVariables.lotNo = entry2.get()
                staticVariables.csvFileName = staticVariables.lotNo
                staticVariables.cableType = '4.5F_Inner_Jacket'
                #print('4.5F Inner default selected')
                setPath()
        
        staticVariables.OnGraphPage = False
        self.title("Real-time Extrusion Grapher")
        self.geometry('250x200+550+200')  
              
        fillerframe = tk.Frame(self, height = 250) 
        fillerframe.pack()      
        loginLbl = tk.Label(self, text = "Login Screen", font = (None, 30, 'bold'))
        loginLbl.pack(pady=25)
  
        lab = tk.Label(self, text="Graph Parameters", font=(None, 20))
        group = ttk.LabelFrame(self)   #frame containing main parameters
        group.pack() 
        group.config(labelwidget=lab)


        lbl1 = tk.Label(group, text="Operator", font=(None, 30))                    #Operator
        lbl1.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)      
        entry1 = tk.Entry(group,font=(None, 30))
        entry1.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        
        lbl2 = tk.Label(group, text="Lot No.", font=(None, 30))                     #Lot number
        lbl2.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)          
        entry2 = tk.Entry(group,font=(None, 30))
        entry2.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.option_add("*TCombobox*Listbox*Font", staticVariables.dropdown_font)   #Comboboxes are comprised of listboxed. All list boxes to have specified font.
        lbl3 = tk.Label(group, text="Cable", font=(None, 30))                       #CableType
        lbl3.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)   
        cbo = ttk.Combobox(group, state='readonly', font=(None, 30))                       
        cbo['values'] = ('4.5F Inner Jacket', '4.5F Outer Jacket', '6F Inner Jacket','6F Outer Jacket', '7.5F Inner Jacket', '7.5F Outer Jacket', 'Other')
        cbo.current(0)
        cbo.bind("<<ComboboxSelected>>",getValue)
        cbo.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        btnFrame = tk.Frame(self)                                  #buttons
        btnFrame.pack()
        btn1 = tk.Button(btnFrame, text='Start',font = staticVariables.btnfont, command=showGraph1)
        btn1.grid(row=0,column=0, padx=10, pady=10)
        btnQuit = tk.Button(btnFrame, text='Quit',font = staticVariables.btnfont, command=quit)
        btnQuit.grid(row=0,column=1,padx=10, pady=10) 
        getDataFields()   #grab selected cable type

        #toggle screen sizes
        self.state = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        #self.geometry('900x900+500+100')
        self.attributes("-fullscreen",True)
    
    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)
        return "break"   

class currentYReading(tk.Label):     #display current Zumbach reading
    def __init__(self,parent):
        tk.Label.__init__(self,parent, text = staticVariables.currentXReading, font = ("Courier", 40),fg="blue")
        #self.text="hello"                   #Operator                    btnStop.config(state = 'normal')
        self.pack()

        def getCurrent():
            self.config(text = staticVariables.currentYReading)
            #print("hellooo")
            self.after(800,getCurrent)  #every 800 ms call getCurrent method in a seperate thread
        getCurrent()

   
class FixedInterval(tk.Tk):  #DynamicPage inherits from Frame class. DynamicPage 'is a' Frame
    procStatus = False
    def __init__(self): #override the frame cosntructor
        tk.Tk.__init__(self)     # child must explicitly call parent constructor. 'Frame' is the parent class.
        def switchGraph():
            staticVariables.isPaused = False
            print('isPaused is ' + str(staticVariables.isPaused))
            app = EntireGraph()
            self.destroy()
            aniObj = AnimateEntireGraph(staticVariables.UCL, staticVariables.LCL, 0, 0)
            staticVariables.aniObj = animation.FuncAnimation(staticVariables.fig, aniObj.animate, interval = 1000)
            tk.mainloop()

        def quit():
            btnQuit.config(state = tk.DISABLED)
            self.result = messagebox.askyesno('Are you sure?', 'Quitting will cause the system to shut down.')
            if self.result == True:
                call("sudo nohup shutdown -h now", shell=True)
            else:
                btnQuit.config(state = 'normal')     

        def stop():
            staticVariables.isPaused = True
            btnStop.config(state = tk.DISABLED)
            result = messagebox.askyesno('Are you sure?',"Once you stop you can't continue recording..")
            if result == True:
                staticVariables.isStopped = True
                p = psutil.Process(staticVariables.pid)             #terminate graphing
                p.terminate()
                try:
                    setPath()
                    copyFile()
                    staticVariables.isPaused = False
                except:
                    messagebox.showerror('error', 'could not copy .csv file to server')
                    pause()
                    staticVariables.isPaused = False
            else:
                btnStop.config(state = 'normal')
                staticVariables.isPaused = not staticVariables.isPaused
                
        def pause():
            staticVariables.isPaused = not staticVariables.isPaused
            if staticVariables.isPaused == True:
                btnPause.config(text = 'Resume')
            else:
                btnPause.config(text = 'Pause')
        
        def goHome():
            btnHome.config(state = tk.DISABLED)
            result = messagebox.askyesno('Are you sure?',"This will terminate your current session..")
            if result == True:
                app = LoginPage()
                self.destroy()
                tk.mainloop()
            else:
                btnHome.config(state = 'normal')

        def center(toplevel):
            toplevel.update_idletasks()
            w = toplevel.winfo_screenwidth()
            h = toplevel.winfo_screenheight()
            size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
            x = w/2 - size[0]/2
            y = h/2 - size[1]/2
            toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))  #giving the window a size does not work because children are using pack
        
        #self.geometry('700x630+550+200')
        #conn = checkConnection()
        staticVariables.OnGraphPage = True
        label = tk.Label(self, text="Previous 1200 datapoints", font= staticVariables.bigText)   #create label object
        label.pack(pady=10)
        frame = tk.Frame(self)      #used for current reading
        frame.pack(fill=tk.X)       #take up assigned space
        filler = tk.Frame(frame)    
        filler.pack(side=tk.LEFT, fill = tk.X, expand = 1)  #tell manager to asign and fill as much space as possible to filler, leaving the minimum for 'group'.   

        lab = tk.Label(self, text="Current Reading", font=(None, 20))             
        group = ttk.LabelFrame(frame)   #frame containing main parameters
        group.pack(side=tk.LEFT,fill = tk.X, padx = 300)    #take up as much space as available (which is miminimal)
        group.config(labelwidget=lab)
        lbl = currentYReading(group)

        fixedGraph = subGraphingRoutine(self)
        fixedGraph.pack(fill=tk.BOTH, expand = 1)
        frm = tk.Frame(self)
        frm.pack()
        btnShow = tk.Button(frm, text="Show entire graph",font = staticVariables.btnfont, command=switchGraph)  #lambda allows you to reference functions which require arguments (in buttons)     
        btnShow.grid(row=0,column=0)  #button is organized into a blocks similar to HTML
        btnHome = tk.Button(frm, text="Home",font = staticVariables.btnfont, command=goHome)  #lambda allows you to reference functions which require arguments (in buttons)     
        btnHome.grid(row=0,column=1,padx=25)  #button is organized into a blocks similar to HTML
        btnPause = tk.Button(frm, text="Pause",font = staticVariables.btnfont, command=pause)  #lambda allows you to reference functions which require arguments (in buttons)     
        btnPause.grid(row=0,column=2)  #button is organized into a blocks similar to HTML
        btnStop = tk.Button(frm, text="STOP",font = staticVariables.btnfont, command=stop)  #lambda allows you to reference functions which require arguments (in buttons)     
        btnStop.grid(row=0,column=3,padx=25)  #button is organized into a blocks similar to HTML
        btnQuit = tk.Button(frm, text="Quit",font = staticVariables.btnfont, command=quit)  #lambda allows you to reference functions which require arguments (in buttons)     
        btnQuit.grid(row=0,column=4)  #button is organized into a blocks similar to HTML

        if staticVariables.isStopped == True:
            btnStop['state'] = tk.DISABLED
        if staticVariables.isPaused == True:
            btnPause.config(text = 'Resume')
        else:
            btnPause.config(text = 'Pause')

        #toggle screen sizes
        self.state = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        #self.geometry('900x900+500+100')
        self.attributes("-fullscreen",True)
    
    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)
        return "break"   


class EntireGraph(tk.Tk):        
    def __init__(self): #override the frame cosntructoras
        tk.Tk.__init__(self)     # child must explicitly call parent constructor. 'Frame' is the parent class.
        def switchGraph():
            staticVariables.isPaused = False
            print('isPaused is ' + str(staticVariables.isPaused))
            app = FixedInterval()
            self.destroy()
            aniObj = Animate(1200, staticVariables.UCL, staticVariables.LCL, 0, 0)
            staticVariables.aniObj = animation.FuncAnimation(staticVariables.fig, aniObj.animate, interval = 1000)
            tk.mainloop()

        def quit():
            btnQuit.config(state = tk.DISABLED)
            self.result = messagebox.askyesno('Are you sure?', 'Quitting will cause the system to shut down.')
            if self.result == True:
                call("sudo nohup shutdown -h now", shell=True)
            else:
                btnQuit.config(state = 'normal')     
                
        def stop():
            pause()
            btnStop.config(state = tk.DISABLED)
            result = messagebox.askyesno('Are you sure?',"Once you stop you can't continue recording..")
            if result == True:
                staticVariables.isStopped = True
                p = psutil.Process(staticVariables.pid)             #terminate graphing
                p.terminate()
                try:
                    setPath()
                    copyFile()
                    pause()
                except:
                    messagebox.showerror('error', 'could not copy .csv file to server')
                    staticVariables.isPaused = not staticVariables.isPaused
            else:
                btnStop.config(state = 'normal')
                staticVariables.isPaused = not staticVariables.isPaused
                pause()
                
        def pause():
            staticVariables.isPaused = not staticVariables.isPaused
            if staticVariables.isPaused == True:
                btnPause.config(text = 'Resume')
            else:
                btnPause.config(text = 'Pause')
        
        def goHome():
            btnHome.config(state = tk.DISABLED)
            result = messagebox.askyesno('Are you sure?',"This will terminate your current session..")
            if result == True:
                app = LoginPage()
                self.destroy()
                tk.mainloop()
            else:
                btnHome.config(state = 'normal')

        def center(toplevel):
            toplevel.update_idletasks()
            w = toplevel.winfo_screenwidth()
            h = toplevel.winfo_screenheight()
            size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
            x = w/2 - size[0]/2
            y = h/2 - size[1]/2
            toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

        #self.geometry('700x630+550+200')
        staticVariables.OnGraphPage = True
        label = tk.Label(self, text="Entire Graph", font=staticVariables.bigText)   #create label object
        label.pack(pady=10)
        frame = tk.Frame(self)      #used for current reading
        frame.pack(fill=tk.X)       #take up assigned space
        filler = tk.Frame(frame)    
        filler.pack(side=tk.LEFT, fill = tk.X, expand = 1)  #tell manager to asign and fill as much space as possible to filler, leaving the minimum for 'group'.     
        
        lab = tk.Label(self, text="Current Reading", font=(None, 20))      
        group = ttk.LabelFrame(frame, text="Current Reading")   #frame containing main parameters
        group.pack(side=tk.LEFT,fill = tk.X, padx = 300)    #take up as much space as available (which is miminimal)
        lbl = currentYReading(group)
        group.config(labelwidget=lab)       

        entireGraph = subGraphingRoutine(self)
        entireGraph.pack(fill=tk.BOTH, expand = 1)
        frm = tk.Frame(self)
        frm.pack()   
        btnShow = tk.Button(frm, text="Show Fixed graph",font = staticVariables.btnfont, command=switchGraph)  #lambda allows you to reference functions which require arguments (in buttons)     
        btnShow.grid(row=0,column=0)  
        btnHome = tk.Button(frm, text="Home",font = staticVariables.btnfont, command=goHome)  #lambda allows you to reference functions which require arguments (in buttons)     
        btnHome.grid(row=0,column=1,padx=25)  #button is organized into a blocks similar to HTML
        btnPause = tk.Button(frm, text="Pause",font = staticVariables.btnfont, command=pause)  #lambda allows you to reference functions which require arguments (in buttons)     
        btnPause.grid(row=0,column=2)  #button is organized into a blocks similar to HTML
        btnStop = tk.Button(frm, text="STOP",font = staticVariables.btnfont, command=stop)  #lambda allows you to reference functions which require arguments (in buttons)     
        btnStop.grid(row=0,column=3,padx=25)  #button is organized into a blocks similar to HTML
        btnQuit = tk.Button(frm, text="Quit",font = staticVariables.btnfont, command=quit)  #lambda allows you to reference functions which require arguments (in buttons)     
        btnQuit.grid(row=0,column=4)  #button is organized into a blocks similar to HTML

        if staticVariables.isStopped == True:
            btnStop['state'] = tk.DISABLED
        if staticVariables.isPaused == True:
            btnPause.config(text = 'Resume')
        else:
            btnPause.config(text = 'Pause')

        #toggle screen sizes
        self.state = False
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        #self.geometry('900x900+500+100')
        self.attributes("-fullscreen",True)
    
    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)
        return "break"   

              
class Animate(object):    #animate 6F object
    xcoord = 0.0
    ycoord = 0.0
    lcl_ycoord = 0.0
    ucl_ycoord = 0.0

    def __init__(self, xInterval, ucl, lcl, usl, lsl):  
        global xInterval_val, ucl_val, lcl_val, usl_val, lsl_val
        xInterval_val = xInterval
        ucl_val = ucl
        lcl_val = lcl
        usl_val = usl
        lsl_val = lsl
        print('Animate object created')
    
    @classmethod
    def alternateConstructor(cls, ucl, lcl, usl, lsl):
        ucl_val = ucl
        lcl_val = lcl
        usl_val = usl
        lsl_val = lsl
        return cls(None, ucl_val, lcl_val, usl_val, lsl_val)

    count = 0
    elapsed = 0
    def animate(self, i): #i for 'interval'
        if staticVariables.isPaused == True:
            pass
        else:
            start_time = timeit.default_timer() #start timer
            graph_data = open(staticVariables.localPath,'r').read()  #open samplefile with the intention to read
            lines = graph_data.split('\n')
            ys = [None]*xInterval_val #y-axis collection
            xs = [None]*xInterval_val
            ucl = [None]*xInterval_val
            lcl = [None]*xInterval_val
            if len(lines) >= xInterval_val:
                for line in reversed(lines):   
                    if len(line)>1: #check that line isnt't totally empty
                        x,y = line.split(',')
                        xs[xInterval_val - staticVariables.tracker] = x    #attach/insert new list onto the x-axis collection
                        ys[xInterval_val - staticVariables.tracker] = y    #attach/insert new list onto the y-axis collection
                        ucl[xInterval_val - staticVariables.tracker] = ucl_val
                        lcl[xInterval_val - staticVariables.tracker] = lcl_val
                        staticVariables.currentYReading = str(ys[xInterval_val-1])
                        staticVariables.currentXReading = str(xs[xInterval_val-1])
                        self.xcoord = ('%.3f' % float(staticVariables.currentXReading))
                        self.ycoord = ('%.3f' % float(staticVariables.currentYReading))
                        self.lcl_ycoord = ('%.3f' % float(lcl_val))
                        self.ucl_ycoord = ('%.3f' % float(ucl_val))
                        staticVariables.tracker = staticVariables.tracker + 1
                        if staticVariables.tracker > 1200:
                            staticVariables.tracker = 1 #reset tracker      
                            break
                staticVariables.ax1.clear()
                staticVariables.ax1.plot(xs, ys)
                staticVariables.ax1.set_title(staticVariables.operator + ' | ' + staticVariables.lotNo + ' | ' + staticVariables.cableType, size = 20)
                staticVariables.ax1.set_xlabel('Time (s)', size = 20, weight ='bold')
                staticVariables.ax1.set_ylabel('Outer diameter (mm)', size = 20, weight ='bold')
                staticVariables.ax1.plot(xs, ucl, linewidth=1, label='UCL', color='r')  
                staticVariables.ax1.plot(xs, lcl, linewidth=1, label='LCL', color='r')
                staticVariables.ax1.annotate('OD = ' + str(self.ycoord), xy = (self.xcoord, self.ycoord),fontsize=20)
                staticVariables.ax1.annotate('LCL = ' + str(self.lcl_ycoord), xy = (self.xcoord, self.lcl_ycoord),fontsize=20)
                staticVariables.ax1.annotate('UCL = ' + str(self.ucl_ycoord), xy = (self.xcoord, self.ucl_ycoord),fontsize=20)
            else:
                for line in lines:   
                    if len(line)>1: #check that line isnt't totally empty
                        x,y = line.split(',')
                        xs.append(x)    #attach/insert new list onto the x-axis collection
                        ys.append(y)    #attach/insert new list onto the y-axis collection
                        ucl.append(ucl_val) 
                        lcl.append(lcl_val)
                        staticVariables.currentYReading = str(y)
                        staticVariables.currentXReading = str(x)
                        self.xcoord = ('%.3f' % float(staticVariables.currentXReading))
                        self.ycoord = ('%.3f' % float(staticVariables.currentYReading))
                        self.lcl_ycoord = ('%.3f' % float(lcl_val))
                        self.ucl_ycoord = ('%.3f' % float(ucl_val))
                staticVariables.ax1.clear()
                staticVariables.ax1.plot(xs, ys)
                staticVariables.ax1.set_title(staticVariables.operator + ' | ' + staticVariables.lotNo + ' | ' + staticVariables.cableType, size = 20)
                staticVariables.ax1.set_xlabel('Time (s)', size = 20, weight ='bold')
                staticVariables.ax1.set_ylabel('Outer diameter (mm)', size = 20, weight ='bold')
                staticVariables.ax1.plot(xs, ucl, linewidth=1, label='UCL', color='r')  
                staticVariables.ax1.plot(xs, lcl, linewidth=1, label='LCL', color='r')
                staticVariables.ax1.annotate('OD = ' + str(self.ycoord), xy = (self.xcoord, self.ycoord),fontsize=20)
                staticVariables.ax1.annotate('LCL = ' + str(self.lcl_ycoord), xy = (self.xcoord, self.lcl_ycoord),fontsize=20)
                staticVariables.ax1.annotate('UCL = ' + str(self.ucl_ycoord), xy = (self.xcoord, self.ucl_ycoord),fontsize=20)                                          

class AnimateEntireGraph(Animate):    #animate 6F object
    xcoord = 0.0
    ycoord = 0.0
    lcl_ycoord = 0.0
    ucl_ycoord = 0.0
    def __init__(self, ucl, lcl, usl, lsl):  
        Animate.alternateConstructor(ucl, lcl, usl, lsl)

    def animate(self, j): #i for 'interval'
        if staticVariables.isPaused == True:
            pass
        else:
            graph_data = open(staticVariables.localPath,'r').read()  #open samplefile with the intention to read
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
                    staticVariables.currentYReading = str(y)
                    staticVariables.currentXReading = str(x)
                    self.xcoord = ('%.3f' % float(staticVariables.currentXReading))
                    self.ycoord = ('%.3f' % float(staticVariables.currentYReading))
                    self.lcl_ycoord = ('%.3f' % float(lcl_val))
                    self.ucl_ycoord = ('%.3f' % float(ucl_val))
            staticVariables.ax1.clear()
            staticVariables.ax1.plot(xs, ys)
            staticVariables.ax1.set_title(staticVariables.operator + ' | ' + staticVariables.lotNo + ' | ' + staticVariables.cableType, size = 20)
            staticVariables.ax1.set_xlabel('Time (s)', size = 20, weight ='bold')
            staticVariables.ax1.set_ylabel('Outer diameter (mm)', size = 20, weight ='bold')
            staticVariables.ax1.plot(xs, ucl, linewidth=1, label='UCL', color='r')  
            staticVariables.ax1.plot(xs, lcl, linewidth=1, label='LCL', color='r')
            #staticVariables.ax1.legend(bbox_to_anchor=(1.005, 1), loc=2, borderaxespad=0.)
            staticVariables.ax1.annotate('OD = ' + str(self.ycoord), xy = (self.xcoord, self.ycoord),fontsize=20)
            staticVariables.ax1.annotate('LCL = ' + str(self.lcl_ycoord), xy = (self.xcoord, self.lcl_ycoord),fontsize=20)
            staticVariables.ax1.annotate('UCL = ' + str(self.ucl_ycoord), xy = (self.xcoord, self.ucl_ycoord),fontsize=20)
            if staticVariables.isStopped == True:   #if stopped refresh graph once
                print('refresh graph damnit')
                staticVariables.isPaused = True         

def checkFile():
    try:
        graph_data =  open(staticVariables.localPath,'r').read()
        lines = graph_data.split('\n')
        xs = []
        for line in lines:   
            if len(line)>1:
                x,y = line.split(',')
                staticVariables.mostRecent_xvalue = x
        print('most recent x value is ' + str(staticVariables.mostRecent_xvalue))                
    except FileNotFoundError:
        if staticVariables.connectionError == False and staticVariables.permissionError == False:     #only create a new file if there is no file existing and there are no zumbach errors
            with open(staticVariables.localPath, 'a') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

def checkConnection():
    try:
        print('checking connection')
        arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
        print('connection establised')
        arduino.close()
        print('connection closed')
        return True
    except:
        return False


class ReadandWrite(object):
    adruino = None
    x = 0
    connectionError = None
    permissionError = None
    count = 0
    localPath =''
    y = 0
    pid = 0
    items = ()
    elapsed = 0

    def __init__(self):
        self.x = float(staticVariables.mostRecent_xvalue)
        self.elapsed = self.x 
        self.connectionError = staticVariables.connectionError
        self.permissionError = staticVariables.permissionError
        self.localPath = staticVariables.localPath
    
        
    def runprocess(self,q,conn):
        print('4 - process has been spawned')    
        self.pid = os.getpid()
        conn.send(self.pid)

        while True:
            try:
                if (self.connectionError == False and self.permissionError == False):
                    if self.count < 1:  #connect once
                        self.adruino = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
                        print('connected')
                        self.count = 1   
                    serialcmd = 'g210'
                    self.adruino.write(serialcmd.encode())
                    response = self.adruino.readline().decode('utf-8').rstrip()  #rstrip() removes all characters from before and after the string
                    with open(self.localPath, 'a', newline='') as csvfile:     #'a' for appending, 'w' for overriding (erase all then write) and 'r' for readonly
                        if len(response) > 0:
                            text,y = response.split(' ')
                            self.y = y
                            fieldnames = ['x_axis', 'y_axis']   #x and y headers
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames) # DictWriter does same thing as a writerclass
                            try:
                                self.elapsed = (timeit.default_timer() - start_time)  + self.x   #offset by the most recent xvalue after connection is lost and re-established
                                writer.writerow({'x_axis': str(self.elapsed), 'y_axis': str(y)})  
                            except:    
                                writer.writerow({'x_axis': str(self.elapsed), 'y_axis': str(y)})     
                                start_time = timeit.default_timer() #start timer                             
            except Exception as e:
                #print(str(e))
                self.items = (e)
                time.sleep(0.5)
                q.put(self.items)
                time.sleep(0.5)
                staticVariables.readySwitch = False
                p = psutil.Process(self.pid)
                try:
                    self.adruino.close()
                except:
                    pass
                p.terminate()
                #pass

def loopProcess():
    staticVariables.queue = Queue()
    staticVariables.parent, staticVariables.child = Pipe()
    condition = ReadandWrite()   #grab static variables 
    proc = Process(target=condition.runprocess, args=(staticVariables.queue, staticVariables.child))   #spawn a seperate append process.     
    proc.start()  
    staticVariables.error = staticVariables.queue.get()                                               


class SerialCommunication(Thread):
    queue = None
    count = 0

    def __init__(self):    #disconnect during use
        #count = 0
        #queue = Queue()
        while staticVariables.isStopped == False:
            try:                             
                while True:
                    try:
                        if self.count < 1:
                            Thread(target=loopProcess).start()         
                            time.sleep(1)
                            staticVariables.pid = staticVariables.parent.recv()
                            print('pid is ' + str(staticVariables.pid))  
                        self.count = 1  #count doesnt change to one unless pid is retrieved without errors.
                    except:
                        pass      
                    if staticVariables.error != None:
                        print(str(staticVariables.error))
                        raise staticVariables.error  
                    if staticVariables.OnGraphPage == False and staticVariables.pid != 0:
                        print('Terminating SerialCommunication')
                        break
                    #print('serial com loop')
            except serial.SerialException as e:
                if staticVariables.OnGraphPage == True:
                    staticVariables.connectionError = True 
                    while True:
                        messagebox.showerror("Error", "Check Zumbach connection!")
                        conn = checkConnection()
                        if conn == True:
                            break
                    checkFile() #check file to continue from most recent x value
                    staticVariables.connectionError = False 
                    staticVariables.error = None
                    self.count = 0
            except PermissionError:
                if staticVariables.OnGraphPage == True:
                    arduino.close()
                    messagebox.showerror("Error", "Close .CSV file!")
                    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
                    checkFile()
                    self.count = 0       
            except: #all other errors
                if staticVariables.OnGraphPage == True:
                    staticVariables.connectionError = True 
                    while True:
                        messagebox.showerror("Error", "Check Zumbach connection!")
                        conn = checkConnection()
                        if conn == True:
                            break
                    checkFile() #check file to continue from most recent x value
                    staticVariables.connectionError = False 
                    staticVariables.error = None
                    staticVariables.readySwitch = False
                    self.count = 0

def recordValues():
    i = 0
    a = 18119   #last 200 seconds (3 mins)
    b = 1.9
    while (i >= 0):
        time.sleep(1);
        print(str(i))
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

  
if __name__ == "__main__":
    app = LoginPage()
    tk.mainloop()
 