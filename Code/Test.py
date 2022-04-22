from mpl_toolkits import mplot3d
from matplotlib import pyplot
import numpy as np
from stl import mesh

# Define the 8 vertices of the cube
vertices = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [0, 1, 0], ])
# Define the 12 triangles composing the cube
faces = np.array([
    [0, 1, 2]])

# Create the mesh
cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    print(i)
    print(f)
    for j in range(3):
        cube.vectors[i][j] = vertices[f[j], :]
        print(vertices[f[j], :])


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
