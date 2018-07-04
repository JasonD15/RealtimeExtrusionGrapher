import csv
import serial
import time
import os
from tkinter import messagebox

#fileName = '1153_testV2csv.csv'
#try:
#    graph_data = open('%s' %fileName,'r').read()
#    print('file exists')
#except FileNotFoundError as e:
#    messagebox.showerror("File does not exist Error", e)

#arduino = serial.Serial('COM5', 9600, timeout=.1)   #connection object
#serialcmd = 'g210'
#time.sleep(1)
#receiveListy=[]
#receiveListx=[]

#for i in range(10):
#    arduino.write(serialcmd.encode())
#    response = arduino.readline().decode('utf-8').rstrip()  #rstrip() removes all characters from before and after the string
#    x,y = response.split(' ')
#    receiveListx.append(x)
#    receiveListy.append(y)
##receiveList = [x.rstrip() for x in receiveList]
#print(receiveListx)
#print(receiveListy)

    #create connection object    
    #check for file
    #if file doesnt exist create one

try:
    arduino = serial.Serial('COM5', 9600, timeout=.1)   #set object parameters
    time.sleep(1)
    serialcmd = 'g210'
    for i in range(10):
        arduino.write(serialcmd.encode())
        response = arduino.readline().decode('utf-8').rstrip()  #rstrip() removes all characters from before and after the string
        x,y = response.split(' ')
        with open('1153_testV2csv.csv', 'a', newline='') as csvfile:     #'a' for appending, 'w' for overriding (erase all then write) and 'r' for readonly
            fieldnames = ['x_axis', 'y_axis']   #x and y headers
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames) # DictWriter does same thing as a writerclass
            #writer.writeheader()    #add column titles
            writer.writerow({'x_axis': str(x), 'y_axis': str(y)})                   
except FileNotFoundError as e:
    messagebox.showerror("File does not exist Error", e)       


