import pyglet
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.framebufferobjects import *
import lego
import tasks
import numpy as np
import expmap
import scipy.optimize
import pylab
import mpl_toolkits.mplot3d.axes3d as mp3

width = 256
height = 256


def getcontext():
	global window
	try: window.close()
	except: pass
	window = pyglet.window.Window(width=width, height=height)
	
getcontext()

rotmat = np.array([
[ 0.84804809, -0.20705596,  0.48779327,  0.        ],
[ 0.        ,  0.92050487,  0.39073113,  0.        ],
[-0.52991927, -0.33135879,  0.78063238,  0.        ],
[ 0.        ,  0.        , -0.80000001,  1.        ]]).transpose()

r0 = expmap.rot2axis(rotmat[:3,:3])
#r1 = r0 + np.array([0.3,0.3,0.3])
r1 = r0 + (np.random.rand(3)*2-1)*0.3

rm0 = np.array(rotmat); rotmat[:3,:3] = expmap.axis2rot(r0)
rm1 = np.array(rm0); rm1[:3,:3] = expmap.axis2rot(r1)

def draw(rotmat):
	clearcolor = [0,0,0,0]
	glClearColor(*clearcolor)
	glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
	glEnable(GL_DEPTH_TEST)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(60, 1, 0.3,20)
	glMatrixMode(GL_MODELVIEW)
	glLoadMatrixf(rotmat.transpose())
	lego.draw_pieces(tasks.taskconfig.model)
	global depthim
	depthim = glReadPixels(0, 0, width, height, GL_DEPTH_COMPONENT, GL_FLOAT)
	depthim = 1/depthim[::-1,:]
	window.flip()
draw(rotmat)
d1 = depthim

# Compute the cost funtion given two depth images
# Sum squared difference of distance
def depthcost(im1, im2):
	return np.sum((im1 - im2)**2)
	
def solvepose():
	def err(x):
		rot = np.array(rotmat)
		rot[:3,:3] = expmap.axis2rot(x)
		draw(rot)
		return depthcost(d1, depthim)
	global xs
	xs = scipy.optimize.fmin(err, r1)
	
def surface():
	rangex = np.arange(-0.3,0.3,0.03)
	rangey = np.arange(-0.3,0.3,0.03)
	global x,y
	x,y = np.meshgrid(rangex, rangey)
	
	def err(x):
		rot = np.array(rotmat)
		rot[:3,:3] = expmap.axis2rot(x)
		draw(rot)
		return depthcost(d1, depthim)
	
	global z	
	z = [err(r0+np.array([xp,yp,0])) for xp in rangex for yp in rangey]
	z = np.reshape(z, (len(rangey),len(rangex)))
	fig = pylab.figure(1)
	fig.clf()
	global ax
	ax = mp3.Axes3D(fig)

	ax.plot_surface(x,y,z, rstride=1,cstride=1, cmap=pylab.cm.jet,
		linewidth=0,antialiased=False)
	#ax.scatter(xs.flatten(), ys.flatten(), zs.flatten())
	fig.show()
	
	
def showpointcloud():
	fig = pylab.figure(1)
	fig.clf()
	ax = mp3.Axes3D(fig)
	global x,y
	x,y = np.meshgrid(range(depthim.shape[1]),range(depthim.shape[0]))
	xs,ys,zs = x[::5,::5], y[::5,::5], depthim[::5,::5]
	ax.plot_surface(xs,ys,zs, rstride=1,cstride=1, cmap=pylab.cm.jet,
		linewidth=0,antialiased=False)
	#ax.scatter(xs.flatten(), ys.flatten(), zs.flatten())
	fig.show()