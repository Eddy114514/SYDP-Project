from mpl_toolkits import mplot3d
from matplotlib import pyplot
import numpy as np
from stl import mesh
from scipy.integrate import quad
from PIL import Image, ImageTk
from sympy import *

vert = []
vert_o = []
def f(x): return 14*(x/10)**5
def fo(x): return 15*(x/11)**5


for i in range(2):
    v = []
    vo = []
    for i in range(0, 12):
        if(i <= 10):
            v.append([i, f(i), 0])
        vo.append([i, fo(i), 0])
    vert.append(v)
    vert_o.append(vo)


print(len(vert[0]))
print(len(vert_o[1]))

# Sign Front and Back
face_counter = 0
cube = mesh.Mesh(np.zeros(len(vert[0])-1, dtype=mesh.Mesh.dtype))
for i in range(len(vert[0])-1):
    cube.vectors[i][0] = vert[0][i]
    cube.vectors[i][1] = vert[1][i]
    cube.vectors[i][2] = vert[0][i+1]


"""

# Create the mesh

for i, f in enumerate(faces):
    for j in range(3):
        cube.vectors[i][j] = vertices[f[j], :]

"""

#cube.save('cube.stl')

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
