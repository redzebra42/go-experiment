import tkinter as tk
from tkinter import ttk
root = tk.Tk()
frm = ttk.Frame(root, padding=10)
frm.grid(padx=0, pady=0)
tile = tk.PhotoImage(file ='tkinter/tile.png')
top_left = tk.PhotoImage(file ='tkinter/top_left_corner.png')
top_right = tk.PhotoImage(file ='tkinter/top_right_corner.png')
bottom_left = tk.PhotoImage(file ='tkinter/bottom_left_corner.png')
bottom_right = tk.PhotoImage(file ='tkinter/bottom_right_corner.png')
top = tk.PhotoImage(file ='tkinter/top.png')
bottom = tk.PhotoImage(file ='tkinter/bottom.png')
right = tk.PhotoImage(file ='tkinter/right.png')
left = tk.PhotoImage(file ='tkinter/left.png')
x_tile = tk.PhotoImage(file ='tkinter/x_tile.png')
black_stone = tk.PhotoImage(file ='tkinter/black_stone.png')
white_stone = tk.PhotoImage(file ='tkinter/white_stone.png')

ttk.Button(frm, image=top_left, padding=-3.5, command=root.destroy).grid(column=0, row=0)
ttk.Button(frm, image=top_right, padding=-3.5, command=root.destroy).grid(column=18, row=0)
ttk.Button(frm, image=bottom_left, padding=-3.5, command=root.destroy).grid(column=0, row=18)
ttk.Button(frm, image=bottom_right, padding=-3.5, command=root.destroy).grid(column=18, row=18)
for i in range(1,18):
    ttk.Button(frm, image=top, padding=-3.5, command=root.destroy).grid(column=i, row=0)
for i in range(1,18):
    ttk.Button(frm, image=bottom, padding=-3.5, command=root.destroy).grid(column=i, row=18)
for j in range(1,18):
    ttk.Button(frm, image=left, padding=-3.5, command=root.destroy).grid(column=0, row=j)
for j in range(1,18):
    ttk.Button(frm, image=right, padding=-3.5, command=root.destroy).grid(column=18, row=j)
for i in range(1,18):
    for j in range(1,18):
        if i in [3,9,15] and j in [3,9,15]:
            ttk.Button(frm, image=x_tile, padding=-3.5, command=root.destroy).grid(column=i, row=j)
        else:
            ttk.Button(frm, image=tile, padding=-3.5, command=root.destroy).grid(column=i, row=j)
root.mainloop()

