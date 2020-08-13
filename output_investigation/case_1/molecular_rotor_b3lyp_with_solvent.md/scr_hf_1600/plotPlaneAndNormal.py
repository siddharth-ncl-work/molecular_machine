import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

point  = np.array([10, 0, 0])
normal=np.array([1,0,0.2])
#normal = np.array([-0.89214967,  0.34347699,  0.29341528])
#print(normal)
# a plane is a*x+b*y+c*z+d=0
# [a,b,c] is the normal. Thus, we have to calculate
# d and we're set
normal = normal/np.linalg.norm(normal)
d = -point.dot(normal)

# create x,y
xx, yy = np.meshgrid(range(-10,10), range(-10,10))

# calculate corresponding z
z = (-normal[0] * xx - normal[1] * yy - d) * 1. /normal[2]
print(z)
# plot the surface
plt3d = plt.figure().gca(projection='3d')
plt3d.plot_surface(xx, yy, z)
plt3d.quiver([point[0]],[point[1]],[point[2]],\
[normal[0]],[normal[1]],[normal[2]],length=10,\
normalize=True)
plt.xlabel('x')
plt.ylabel('y')
plt.show()

