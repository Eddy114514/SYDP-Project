from mpl_toolkits import mplot3d
from matplotlib import pyplot
import numpy as np
from stl import mesh
from scipy.integrate import quad
from PIL import Image, ImageTk
from sympy import *


v_listi = []
v_listo = []
vz = []
vzo = []
v_list = []

faces = []
for i in range(0, 10):
    v_listi.append([i, 0, i**2])
for k in range(0, 11):
    v_listo.append([k, 0, k**2])

for i in range(0, 10):
    vzo.append([i, 1, i**2])
for k in range(0, 11):
    vz.append([k, 1, k**2])

for o in v_listo:
    v_list.append(o)
for o in v_listi:
    v_list.append(o)
for o in vzo:
    v_list.append(o)
for o in vz:
    v_list.append(o)

vv_list = [v_listo, v_listi, vzo, vz]
for i in vv_list:
    print(len(i))

# Define the 8 vertices of the cube
vertices = np.array(v_list)
# Define the 12 triangles composing the cube
lensave = 0
count = 0
for j in range(0, len(v_list)):

    # create curve
    if(j == lensave):
        print("yes")
        print(len(vv_list[count]))
        for k in range(lensave, lensave+len(vv_list[count])-2):
            faces.append([k, k+1, k+2])
            print([k, k+1, k+2])
        lensave += len(vv_list[count])
        count += 1
    #creat surface
    print(lensave)

len = [len(vv_list[0]), len(vv_list[1])+len(vv_list[0]), len(vv_list[2])+len(vv_list[1])
       + len(vv_list[0]), len(vv_list[3])+len(vv_list[2])+len(vv_list[1])+len(vv_list[0])]


faces = np.array(faces)
print(faces)

# Create the mesh
cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):

    for j in range(3):
        cube.vectors[i][j] = vertices[f[j], :]
cube.save('cube.stl')

# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Render the cube
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(cube.vectors))

# Auto scale to the mesh size
scale = cube.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)
axes.set_xlabel("X axis")
axes.set_ylabel("Y axis")
axes.set_zlabel("Z axis")


# Show the plot to the screen
pyplot.show()
