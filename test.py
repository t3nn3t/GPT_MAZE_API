# Implementation of matplotlib function 
import matplotlib
matplotlib.use('Qt5Agg')

from mpl_toolkits.mplot3d import axes3d 
import matplotlib.pyplot as plt 

fig = plt.figure() 
ax = fig.add_subplot(111, projection ='3d') 

X, Y, Z = axes3d.get_test_data(0.1) 
ax.plot_wireframe(X, Y, Z, rstride = 5, cstride = 5) 

for angle in range(0, 360): 
	ax.view_init(30, angle) 
	plt.draw() 
	plt.pause(.001) 
	ax.set_title('matplotlib.pyplot.pause() function Example', fontweight ="bold") 
