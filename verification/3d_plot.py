import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


fig = plt.figure()
ax = plt.axes(projection="3d")

z_line = [1,1,1,1,1,2,2,2,2,2]
x_line = [1,2,3,4,5,1,2,3,4,5]
y_line = [1,2,3,4,5,1,2,3,4,5]
ax.scatter3D(x_line, y_line, z_line, 'gray')

'''
z_points = 15 * np.random.random(100)
x_points = np.cos(z_points) + 0.1 * np.random.randn(100)
y_points = np.sin(z_points) + 0.1 * np.random.randn(100)
ax.scatter3D(x_points, y_points, z_points, c=z_points, cmap='hsv');
'''

x=range(11)
y=range(3)

X,Y=np.meshgrid(x,y)
Z=np.ones((3,11))
Z[1,:]=2
Z[2,:]=-2
print(X)
print(Y)
print(Z)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1,cmap='winter', edgecolor='none')
ax.set_title('surface');

plt.show()
