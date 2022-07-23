import numpy as np
from stl import mesh
import matplotlib.pyplot as plt
from tkinter import *
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import messagebox
from matplotlib import pyplot
from mpl_toolkits import mplot3d
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from tkinter import filedialog
root = Tk()
root.title('测试')

root.geometry('1600x1000+10+10')

tab_main=ttk.Notebook()#创建分页栏
tab_main.place(relx=0.02, rely=0.02, relwidth=0.887, relheight=0.876)

tab1=Frame(tab_main)#创建第一页框架

tab1.place(x=0,y=30)
tab_main.add(tab1,text='第一页')#将第一页插入分页栏中

Text = Text(tab1,width = 50,height=40)#显示文本框
Text.place(x=10,y=100)
button = Button(tab1,text='1',width=5)
button.place(x=50,y=10)
button1 = Button(tab1,text='2',width=5)
button1.place(x=100,y=10)
button2 = Button(tab1,text='3',width=5)
button2.place(x=150,y=10)
button3 = Button(tab1,text='4',width=5)
button3.place(x=200,y=10)

# Define the 8 vertices of the cube
vertices = np.array([\
    [-1, -1, -1],
    [+1, -1, -1],
    [+1, +1, -1],
    [-1, +1, -1],
    [-1, -1, +1],
    [+1, -1, +1],
    [+1, +1, +1],
    [-1, +1, +1]])
# Define the 12 triangles composing the cube
faces = np.array([\
    [0,3,1],
    [1,3,2],
    [0,4,7],
    [0,7,3],
    [4,5,6],
    [4,6,7],
    [5,1,2],
    [5,2,6],
    [2,3,6],
    [3,7,6],
    [0,1,5],
    [0,5,4]])

# Create the mesh
cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        cube.vectors[i][j] = vertices[f[j],:]


tab2=Frame(tab_main,bg ="blue")
tab_main.add(tab2,text='第二页')





fig = Figure(figsize=(5, 5),
                     dpi=100)
axes = fig.add_subplot(111, projection="3d")
# Render the canoe
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(cube.vectors))

scale = cube.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)
axes.set_xlabel("X axis")
axes.set_ylabel("Y axis")
axes.set_zlabel("Z axis")

canvas = FigureCanvasTkAgg(fig, tab2)
canvas.draw()
canvas.get_tk_widget().place(relx=0.3,rely=0.1)



root.mainloop()



