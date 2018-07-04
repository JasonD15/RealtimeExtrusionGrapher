import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)    # subplot on a grid system



def animate(j):
    graph_data = open('samplefile.txt','r').read()  #open samplefile with the intention to read
    lines = graph_data.split('\n')
    xs = [] #x-axis collection
    ys = [] #y-axis collection
    xs2 = []
    ys2 = []
    test = ['4','4','4']
    for line in lines:
        if len(line)>1: #check that line isnt't totally empty
            x,y = line.split(',')
            xs.append(x)    #attach/insert new list onto the x-axis collection
            ys.append(y)    #attach/insert new list onto the y-axis collection
            xs2.append(x)
            ys2.append(test)

    ax1.clear()
    ax1.plot(xs, ys) 
    ax1.plot(xs2, ys2) 
  
           

ani = animation.FuncAnimation(fig, animate, interval = 1000)      
# we want to store the object so we asign it to variable 'ani'
#animation.FuncAnimation allows you to animate based on a fucntion,'fig' = where to animate function to, 'animate' - function that we're going to animate, 'interval' = rate
plt.show()