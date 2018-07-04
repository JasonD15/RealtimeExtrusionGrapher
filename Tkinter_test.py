import tkinter as tk
#Each widget in pack manager is assigned one row. Padding is added to the sides as u resize screen.
#'fill' tells the widget to grow and fill in  as much of the assigned/designated space as possible in a specific direction. e.g.fill in the entire row as it was assigned that one row.
#'expand' tells the manager to assigned maximum space to the widget, with the remainder of the space being distributed evenly to the non-expand children widgets.
#Frames 'wrap' their contents by default
root = tk.Tk()
root.geometry('200x200+200+200')
tk.Label(root, text='Label', bg='green').pack(expand=1, fill=tk.Y)
tk.Label(root, text='Label2', bg='red').pack(fill=tk.BOTH)
tk.Label(root, text='Label2', bg='pink').pack(expand=1, fill=tk.BOTH)
root.mainloop()






