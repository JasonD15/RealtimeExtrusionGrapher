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
from multiprocessing import Process
from tkinter import messagebox
import serial
import timeit
import shutil
from subprocess import call

#change to
#Zumbach - 'g210\r\n'
#Zumbach - ('/dev/ttyUSB0',19200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE, timeout=.1)
#Arduino - ('/dev/ttyACM0', 9600, timeout=.1)
#Arduino - ('COM4', 9600, timeout=.1)
#Arduino - ('COM3', 9600, timeout=.1)
#Arduino - 'g210'

class parameterException(Exception):
    def __init__(self,msg):
        Exception.__init__(self, msg)

class staticVariables(object):
    fig = plt.figure()             #variables outside functions are equivalent to static variables     
    ax1 = fig.add_subplot(1,1,1)
    title_font = ("Arial", 20, 'bold')
    parameters_font = ("Times", "16", "bold italic")
    btnfont = ('Sans','10','bold')
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
    notConnectionError = True   #always opposite to connection error.
    permissionError = False
    notPermissionError = True
    aniObj = None
    runtimeConnectionError = False
    OnGraphPage = False     
    killThread = False
    notkillThread = True
    loginCounter = 0
    closeApp = False
    currentReading=0
    localPath=''
    serverPath=''
    isStopped = False

def setPath():
    staticVariables.localPath = '%s/%s_%s.csv' %('C:/Users/Admin/Dropbox/Python/DynamicGraphing/DynamicGraphing', staticVariables.lotNo,staticVariables.operator)
    staticVariables.serverPath = '%s/%s_%s.csv' %('C:/Users/Admin/Dropbox/Python/DynamicGraphing/ExportedGraphs/folder2', staticVariables.lotNo,staticVariables.operator)

def copyFile():
    shutil.copy(staticVariables.localPath, staticVariables.serverPath)

    
class subGraphingRoutine(tk.Frame): 
    def __init__(self, parent):  
        tk.Frame.__init__(self, parent)
        style.use('fivethirtyeight')
        label = ttk.Label(self,text="Real-time Extrusion Grapher", font=staticVariables.title_font).pack() #tkk extends tkinter widget. Create label object.
        canvas = FigureCanvasTkAgg(staticVariables.fig, master=self)
        canvas.get_tk_widget().pack(fill=tk.BOTH,expand=1)
        toolbar = NavigationToolbar2TkAgg(canvas, self )
        toolbar.update()

class LoginPage(tk.Tk):
    def __init__(self):      
        tk.Tk.__init__(self)
        def showGraph1():       #not an instance method, purely a do something methd. Instance methods are inline with the constructor and take self as a default parameter.
            try:
                staticVariables.connectionError = False     #refresh booleans
                staticVariables.notConnectionError = not staticVariables.connectionError
                staticVariables.permissionError = False
                staticVariables.notPermissionError = not staticVariables.permissionError 
                staticVariables.isPaused = False
                staticVariables.isStopped = False

                if len(entry1.get())==0 or len(entry2.get())==0:
                    raise parameterException('Please fill in all fields')
                getDataFields()
                Thread(target = serialCom).start() 
                checkFile()
                while True:
                    if staticVariables.connectionError == True:
                        print("connectionError is true")
                        break
                    elif staticVariables.permissionError == True:
                        messagebox.showerror("Error", "Check .csv file!")
                        break
                    elif (staticVariables.connectionError == False and staticVariables.notConnectionError == True) and (staticVariables.permissionError == False and staticVariables.notPermissionError == True):
                        print("No errors detected")
                        self.destroy()              #destroys reference to object but object still exists.
                        app = FixedInterval()
                        #root = app
                        staticVariables.aniObj = Animate(200, staticVariables.UCL, staticVariables.LCL, 0, 0)
                        ani = animation.FuncAnimation(staticVariables.fig, staticVariables.aniObj.animate, interval = 700)
                        break    
                staticVariables.connectionError = False     #refresh booleans
                staticVariables.notConnectionError = not staticVariables.connectionError
                tk.mainloop()         
            except parameterException as pe:
                messagebox.showerror("Error", pe)
                            
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
                if cboValue == "4.5F - Inner":
                    staticVariables.LCL = 1.400
                    staticVariables.UCL = 1.470
                    staticVariables.operator = entry1.get()
                    staticVariables.lotNo = entry2.get()
                    staticVariables.cableType = '4.5F_Inner'
                    staticVariables.csvFileName = staticVariables.lotNo
                    #print('4.5F selected')
                elif cboValue == "6F - Inner":
                    staticVariables.LCL = 1.085
                    staticVariables.UCL = 1.115
                    staticVariables.operator = entry1.get()
                    staticVariables.lotNo = entry2.get()
                    staticVariables.cableType = '6F_Inner'
                    staticVariables.csvFileName = staticVariables.lotNo
                    #print('6F selected')
                elif cboValue == "7.5F - Inner":
                    staticVariables.LCL = 1.800
                    staticVariables.UCL = 1.840
                    staticVariables.operator = entry1.get()
                    staticVariables.lotNo = entry2.get()
                    staticVariables.cableType = '7.5F_Inner'
                    staticVariables.csvFileName = staticVariables.lotNo
                    #print('6F selected')
                elif cboValue == "4.5F - Outer":
                    staticVariables.LCL = 1.494
                    staticVariables.UCL = 1.544
                    staticVariables.operator = entry1.get()
                    staticVariables.lotNo = entry2.get()
                    staticVariables.cableType = '4.5F_Outer'
                    staticVariables.csvFileName = staticVariables.lotNo
                elif cboValue == "6F - Outer":
                    staticVariables.LCL = 1.875
                    staticVariables.UCL = 1.925
                    staticVariables.operator = entry1.get()
                    staticVariables.lotNo = entry2.get()
                    staticVariables.cableType = '6F_Outer'
                    staticVariables.csvFileName = staticVariables.lotNo
                elif cboValue == "7.5F - Outer":
                    staticVariables.LCL = 2.560
                    staticVariables.UCL = 2.520
                    staticVariables.operator = entry1.get()
                    staticVariables.lotNo = entry2.get()
                    staticVariables.cableType = '7.5F_Outer'
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
                staticVariables.cableType = '4.5F'
                print('4.5F Inner default selected')
                setPath()

        if staticVariables.loginCounter > 0:        #first time login counter is created dont kill serialCom()
            staticVariables.killThread = True       #no serial connection thread running
            staticVariables.notkillThread = not staticVariables.killThread
            print("kill serial thread!")
        staticVariables.loginCounter = 1

        self.title("Real-time Extrusion Grapher")
        self.geometry('250x200+550+200')  
              
        fillerframe = tk.Frame(self, height = 250) 
        fillerframe.pack()      
        loginLbl = tk.Label(self, text = "Login Screen", font = (None, 20, 'bold'))
        loginLbl.pack(pady=25)
  
        group = ttk.LabelFrame(self, text="Graph Parameters")   #frame containing main parameters
        group.pack() 


        lbl1 = tk.Label(group, text="Operator", font=(None, 15))                    #Operator
        lbl1.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)      
        entry1 = tk.Entry(group)
        entry1.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        
        lbl2 = tk.Label(group, text="Lot No.", font=(None, 15))                     #Lot number
        lbl2.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)          
        entry2 = tk.Entry(group)
        entry2.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        lbl3 = tk.Label(group, text="Cable", font=(None, 15))                       #CableType
        lbl3.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)   
        cbo = ttk.Combobox(group, state='readonly')                       
        cbo['values'] = ('4.5F - Inner', '4.5F - Outer', '6F - Inner','6F - Outer', '7.5F - Inner', '7.5F - Outer', 'Other')
        cbo.current(0)
        cbo.bind("<<ComboboxSelected>>",getValue)
        cbo.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        btnFrame = tk.Frame(self)                                  #buttons
        btnFrame.pack()
        btn1 = tk.Button(btnFrame, text='Start',font = staticVariables.btnfont, command=showGraph1)
        btn1.grid(row=0,column=0, padx=10, pady=10)
        btn2 = tk.Button(btnFrame, text='Quit',font = staticVariables.btnfont, command=quit)
        btn2.grid(row=0,column=1,padx=10, pady=10) 
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

class currentReading(tk.Label):     #display current Zumbach reading
    def __init__(self,parent):
        tk.Label.__init__(self,parent, text = staticVariables.currentReading, font = ("Courier", 20))
        #self.text="hello"                   #Operator                    btnStop.config(state = 'normal')
        self.pack()

        def getCurrent():
            self.config(text = staticVariables.currentReading)
            #print("hellooo")
            self.after(700,getCurrent)  #every 700 ms call getCurrent method in a seperate thread
        getCurrent()

class FixedInterval(tk.Tk):  #DynamicPage inherits from Frame class. DynamicPage 'is a' Frame
    def __init__(self): #override the frame cosntructor
        tk.Tk.__init__(self)     # child must explicitly call parent constructor. 'Frame' is the parent class.
        def switchGraph():
            app = EntireGraph()
            staticVariables.killThread = False
            self.destroy()
            aniObj = AnimateEntireGraph(staticVariables.UCL, staticVariables.LCL, 0, 0)
            staticVariables.aniObj = animation.FuncAnimation(staticVariables.fig, aniObj.animate, interval = 700)
            tk.mainloop()

        def quit():
            btnQuit.config(state = tk.DISABLED)
            self.result = messagebox.askyesno('Are you sure?', 'Quitting will cause the system to shut down.')
            if self.result == True:
                call("sudo nohup shutdown -h now", shell=True)
            else:
                btnQuit.config(state = 'normal')                

        def stop():
            btnStop.config(state = tk.DISABLED)
            result = messagebox.askyesno('Are you sure?',"Once you stop you can't continue recording..")
            if result == True:
                #staticVariables.isPaused = True
                staticVariables.isStopped = True
                #print(staticVariables.isStopped)
                try:
                    setPath()
                    copyFile()
                except:
                    print('hello error')
                    messagebox.showerror('error', 'could not copy .csv file to server')
            else:
                btnStop.config(state = 'normal')
                
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
        staticVariables.killThread = False
        staticVariables.OnGraphPage = True
        label = tk.Label(self, text="Previous 200 datapoints", font= staticVariables.title_font)   #create label object
        label.pack(pady=10)
        frame = tk.Frame(self)      #used for current reading
        frame.pack(fill=tk.X)       #take up assigned space
        filler = tk.Frame(frame)    
        filler.pack(side=tk.LEFT, fill = tk.X, expand = 1)  #tell manager to asign and fill as much space as possible to filler, leaving the minimum for 'group'.           
        group = ttk.LabelFrame(frame, text="Current Reading")   #frame containing main parameters
        group.pack(side=tk.LEFT,fill = tk.X, padx = 10)    #take up as much space as available (which is miminimal)
        lbl = currentReading(group)
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
            btnStop['state'] = tk.DISABLED

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
            app = FixedInterval()
            self.destroy()
            aniObj = Animate(200, staticVariables.UCL, staticVariables.LCL, 0, 0)
            staticVariables.aniObj = animation.FuncAnimation(staticVariables.fig, aniObj.animate, interval = 700)
            tk.mainloop()

        def quit():
            btnQuit.config(state = tk.DISABLED)
            self.result = messagebox.askyesno('Are you sure?', 'Quitting will cause the system to shut down.')
            if self.result == True:
                call("sudo nohup shutdown -h now", shell=True)
            else:
                btnQuit.config(state = 'normal')

        def stop():
            btnStop.config(state = tk.DISABLED)
            btnStop.config(state = tk.DISABLED)
            result = messagebox.askyesno('Are you sure?',"Once you stop you can't continue recording..")
            if result == True:
                #staticVariables.isPaused = True
                staticVariables.isStopped = True
                #print(staticVariables.isStopped)
                try:
                    setPath()
                    copyFile()
                except:
                    print('hello error')
                    messagebox.showerror(error, 'could not copy .csv file to server')
            else:
                btnStop.config(state = 'normal')

        def pause():
            staticVariables.isPaused = not staticVariables.isPaused
            if staticVariables.isPaused == True:
                btnPause.config(text = 'Unpause')
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

        self.geometry('700x630+550+200')
        label = tk.Label(self, text="Entire Graph", font=staticVariables.title_font)   #create label object
        label.pack(pady=10)
        frame = tk.Frame(self)      #used for current reading
        frame.pack(fill=tk.X)       #take up assigned space
        filler = tk.Frame(frame)    
        filler.pack(side=tk.LEFT, fill = tk.X, expand = 1)  #tell manager to asign and fill as much space as possible to filler, leaving the minimum for 'group'.           
        group = ttk.LabelFrame(frame, text="Current Reading")   #frame containing main parameters
        group.pack(side=tk.LEFT,fill = tk.X, padx = 10)    #take up as much space as available (which is miminimal)
        lbl = currentReading(group)
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
            btnStop['state'] = tk.DISABLED

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
        if staticVariables.isPaused == True:
            pass
        else:
            graph_data = open(staticVariables.localPath,'r').read()  #open samplefile with the intention to read
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
            staticVariables.ax1.set_title(staticVariables.operator + ' | ' + staticVariables.lotNo + ' | ' + staticVariables.cableType, size = 14)
            staticVariables.ax1.set_xlabel('Time (s)', size = 14, weight ='bold')
            staticVariables.ax1.set_ylabel('Outer diameter (mm)', size = 14, weight ='bold')
            staticVariables.ax1.plot(xs, ucl, linewidth=1, label='UCL', color='r')  
            staticVariables.ax1.plot(xs, lcl, linewidth=1, label='LCL', color='r')
            staticVariables.ax1.legend(bbox_to_anchor=(1.005, 1), loc=2, borderaxespad=0.)
            #staticVariables.ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)

class AnimateEntireGraph(Animate):    #animate 6F object
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
            staticVariables.ax1.clear()
            staticVariables.ax1.plot(xs, ys)
            staticVariables.ax1.set_title(staticVariables.operator + ' | ' + staticVariables.lotNo + ' | ' + staticVariables.cableType, size = 14)
            staticVariables.ax1.set_xlabel('Time (s)', size = 14, weight ='bold')
            staticVariables.ax1.set_ylabel('Outer diameter (mm)', size = 14, weight ='bold')
            staticVariables.ax1.plot(xs, ucl, linewidth=1, label='UCL', color='r')  
            staticVariables.ax1.plot(xs, lcl, linewidth=1, label='LCL', color='r')
            staticVariables.ax1.legend(bbox_to_anchor=(1.005, 1), loc=2, borderaxespad=0.)


def checkFile():
    try:
        graph_data =  open(staticVariables.localPath,'r').read()
        lines = graph_data.split('\n')
        xs = []
        for line in lines:   
            if len(line)>1:
                x,y = line.split(',')
                staticVariables.mostRecent_xvalue = float(x)
    except FileNotFoundError:
        if staticVariables.connectionError == False and staticVariables.permissionError == False:     #only create a new file if there is no file existing and there are no zumbach errors
            with open(staticVariables.localPath, 'a') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

def checkConnection():
    try:
        arduino = serial.Serial('COM4', 9600, timeout=.1)
        return True
    except:
        return False

def serialCom():    #disconnect during use
    count = 0
    arduino = None
    rate = 0.1    #graphs plots 1 dot every 100ms
    while staticVariables.isStopped == False:
        try: 
            if count < 1:   #if no initial connection error then only make exception error once
                arduino = serial.Serial('COM4', 9600, timeout=.1)   #create connection object
            count = 1

            if count < 1 and (staticVariables.connectionError == False and staticVariables.notConnectionError == True) and (staticVariables.permissionError == False and staticVariables.notPermissionError == True): #if errored when trying to log in, once all good then make a connection.
                arduino = serial.Serial('COM4', 9600, timeout=.1)
            time.sleep(1)
            #staticVariables.isPaused = False
            serialcmd = 'g210'
            x = staticVariables.mostRecent_xvalue
            print('most recent value is ' + str(x))
            while staticVariables.isStopped == False:
                if staticVariables.killThread == True and staticVariables.notkillThread == False:
                    return
                elif staticVariables.closeApp == True:
                    raise SystemExit
                start_time = timeit.default_timer()
                arduino.write(serialcmd.encode())
                response = arduino.readline().decode('utf-8').rstrip()  #rstrip() removes all characters from before and after the string
                if len(response) > 0:
                    text,y = response.split(' ')
                    staticVariables.currentReading = y
                    elapsed = (timeit.default_timer() - start_time)
                    x = x + elapsed
                    with open(staticVariables.localPath, 'a', newline='') as csvfile:     #'a' for appending, 'w' for overriding (erase all then write) and 'r' for readonly
                        fieldnames = ['x_axis', 'y_axis']   #x and y headers
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames) # DictWriter does same thing as a writerclass
                        #writer.writeheader()    #add column titles
                        writer.writerow({'x_axis': str(x), 'y_axis': str(y)})
        except serial.SerialException:
            if staticVariables.OnGraphPage == True:
                arduino.close()
                staticVariables.connectionError = True 
                while True:
                    messagebox.showerror("Error", "Check Zumbach connection!")
                    conn = checkConnection()
                    if conn == True:
                        arduino = serial.Serial('COM4', 9600, timeout=.1)
                        break
                checkFile() #check file to continue from most recent x value
            else:
                staticVariables.connectionError = True
                staticVariables.notConnectionError = not staticVariables.connectionError
                staticVariables.isPaused = True
                staticVariables.runtimeConnectionError = True
                messagebox.showerror("Error", "Check Zumbach connection!")
                staticVariables.isPaused = False            #refresh booleans
                staticVariables.connectionError = False     
                staticVariables.notConnectionError = not staticVariables.connectionError
                staticVariables.permissionError = False
                staticVariables.notPermissionError = not staticVariables.permissionError 
                return

        except PermissionError:
            if staticVariables.OnGraphPage == True:
                arduino.close()
                messagebox.showerror("Error", "Close .CSV file!")
                arduino = serial.Serial('COM4', 9600, timeout=.1)
                checkFile()
            else:
                staticVariables.permissionError = True
                staticVariables.notPermissionError = not staticVariables.permissionError 
                messagebox.showerror("Error", "Close .CSV file!")

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
