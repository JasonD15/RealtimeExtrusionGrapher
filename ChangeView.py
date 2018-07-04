import tkinter as tk               # import Tkinter module (class)
from tkinter import font as tkfont # from  Tkinter module (class) import 'font' class


class SampleApp(tk.Tk): #SampleApp inherits from Tkinter. SampleApp 'is a' Tkinter object

    #constructor
    def __init__(self):
        tk.Tk.__init__(self)    #calls constructor for TK class

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        container = tk.Frame(self) #create 'Frame' with master 'self' aka the Tkinter object. Store in container variable.
        container.pack(side="top", fill="both", expand=True)
        #container.grid_rowconfigure(0, weight=1)           #dont use pack and grid in the same container
        #container.grid_columnconfigure(0, weight=1)

        self.frames = {}    # create a dictionary collection of frames, where indexes [X] can be replaced with string references
        for F in (StartPage, PageOne, PageTwo):     
            page_name = F.__name__  #get name of object
            frame = F(parent=container, controller=self)    #create StartPage, PageOne, PageTwo objects. Container is the parent widget and controller is the object being manipulated.
            self.frames[page_name] = frame  #add to frame collection

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise() #bring to top

def printTest(value):
    print("hello jason world" + value)
    #return "hello jason"

class NewFrame(tk.Frame):
    def __init__(self, parent): #create frame
        tk.Frame.__init__(self, parent)
        CustomFont = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        #self.controller = controller    #access a specific font
        #root =tk.Frame(self)
        #root.pack(side="top", fill="both", expand=True)    #creating of a widget must be paired with either pack or grid
        label = tk.Label(self, text="This is a Test Label", font=CustomFont)
        label.pack()


class StartPage(tk.Frame):  #StartPage inherits from Frame class. StartPage 'is a' Frame

    def __init__(self, parent, controller): #override the frame cosntructor
        tk.Frame.__init__(self, parent)     # explicitly calling parent constructor so we can use parent's members. 'Frame' is the parent class
        self.controller = controller    #'controlled by SampleApp object'
        self.root = parent;
        label = tk.Label(self, text="This is the start page", font=controller.title_font)   #create label object
        label.pack(side="top", fill="x", pady=10)
        #create button objects
        self.button1 = tk.Button(self, text="Go to Page One",    
                            command=lambda: controller.show_frame("PageOne"))   #lambda allows you to reference functions which require arguments (in buttons)     
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        self.button1.pack()  #organizes into blocks similar to HTML
        button2.pack()
        button3.pack()
        testObj = NewFrame(self)
        testObj.pack()



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        #self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()