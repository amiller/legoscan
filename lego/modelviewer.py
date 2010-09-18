from lego import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import tasks
import pyreg
import pyglet

def create_window():
	global window
	platform = pyglet.window.get_platform()
	display = platform.get_default_display()
	from pyglet.window import Window
	screen = display.get_default_screen()
	window = Window(width=400, height=400)

# Bind some events for pyglet's event loop
from pyglet.window import key
from pyglet.window import mouse
from OpenGL.GL import *


if __name__ == "__main__":
	try:
		# Don't recreate the window if it's already there!
		window == ''
	except Exception as e:
		#pyglet.clock.schedule_interval(video.frameadvance, 0.03)
		create_window()
		first_run = True
		
fps_display = pyglet.clock.ClockDisplay()

@window.event
def on_key_press(*args, **kwargs):
	_on_key_press(*args, **kwargs)
def _on_key_press(symbol, modifiers):
	if symbol == key.A:
		print 'The "A" key was pressed.'
	elif symbol == key.LEFT:
		print 'The left arrow key was pressed.'
	elif symbol == key.ENTER:
		print 'The enter key was pressed.'
		
@window.event
def on_mouse_press(*args, **kwargs):
	_on_mouse_press(*args, **kwargs)
def _on_mouse_press(x, y, button, modifiers):
    #if button == mouse.LEFT:
		#	print '[%d, %d],' % (x, y)
	pass

@window.event
def on_resize(width_,height_):
	global width, height
	width, height = width_, height_
	glViewport(0,0,width,height)

try: rotangles == ''
except: rotangles = [0, 0]
@window.event
def on_mouse_drag(*args, **kwargs):
	_on_mouse_drag(*args, **kwargs)
def _on_mouse_drag(x, y, dx, dy, buttons, modifiers):
	global drawstopped
	rotangles[0] -= dy
	rotangles[1] += dx
	drawstopped = False

clearcolor = [0,0,0,0]
@window.event
def on_draw():
	if not drawstopped: 
		_on_draw()
		window.flip()
		_on_draw()
def _on_draw():
	
	global drawstopped
	glEnable(GL_DEPTH_TEST)
	glClearColor(*clearcolor)
	window.clear()
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(60, 1, 0.3,20)
	#glOrtho(0,width,0,height,0,20)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	
	# flush that stack
	try:
		while 1: glPopMatrix()
	except:
		pass


	glPushMatrix()
	#if layer > 0:
	#	glTranslate(320,0,0)
	#	factor = 2.0/480
	#	glScale(1+factor,1+factor,1)
	#	glTranslate(-320/(1+factor),0,0)
		
	#glMultMatrixf(homoraphy.transpose())
	
	def mouse_rotate(xAngle, yAngle, zAngle):
		glRotatef(xAngle, 1.0, 0.0, 0.0);
		glRotatef(yAngle, 0.0, 1.0, 0.0);
		glRotatef(zAngle, 0.0, 0.0, 1.0);
	glTranslate(0, 0,-0.8)
	mouse_rotate(rotangles[0], rotangles[1], 0);

	glScale(.05, .05, .07);
	#glEnable(GL_BLEND)
	glDisable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

	if qooim: glBindTexture(qooim.target, qooim.id)

	# Draw the color pieces
	for piece in tasks.taskconfig.model:
		glPushMatrix()
		glTranslate(piece.location[0],piece.location[1],piece.location[2])
		glColor(*piece.color)
		glEnableClientState(GL_VERTEX_ARRAY)
		glEnableClientState(GL_TEXTURE_COORD_ARRAY)
		global cp, indices
		# Draw cube
		glPushMatrix()
		vertices = [[0, 0, 1], [1, 0, 1],	[0, 1, 1],	[1, 1, 1],
								[0, 0, 0], [1, 0, 0],	[0, 1, 0],	[1, 1, 0]];
								
		# Indices for triangle strip around the cube
		glVertexPointers(vertices);
		indices = [0, 1, 2, 3, 7, 1, 5, 4, 7, 6, 2, 4, 0, 1]
		
		glScale(piece.shape[0], piece.shape[1], 1)
		glDrawElementsui(GL_TRIANGLE_STRIP, indices)
		glPopMatrix()
		
		# Circles for the little nubs
		h = np.arange(0,2*np.pi+0.1,0.2)
		h = np.hstack((h, [0]))
		cp = np.hstack((np.vstack((cos(h), sin(h), h*0)),
									  np.vstack((cos(h), sin(h), h*0+1))))
	
		cp = cp.transpose()
		glVertexPointerf(cp)
		
		radius = 0.32
		# outside indices
		indices = np.vstack((range(len(h)), len(h)+np.arange(len(h))))
		indices = indices.transpose().flatten()
		# circle indices
		cindices = range(len(h), len(h)+len(h))
		
		# Texture coordinates for qoo face
		cp[:,0] = (cp[:,0]/1.1 + 1) * qooim.width/2
		cp[:,1] = (cp[:,1]/1.9 + 1 + 0.2) * (qooim.height/2)
 		glTexCoordPointerf(cp[:,:2])
		
		for x in range(piece.shape[0]):
			for y in range(piece.shape[1]):
				glPushMatrix()
				glTranslate(x+0.5, y+0.5, 1)
				glScale(radius, radius, 0.2)
				
				glColor(np.array(piece.color)*0.8)
				glDrawElementsui(GL_TRIANGLE_STRIP, indices)
				
				if qooim and 0: 
					glEnable(qooim.target)
					glColor(1,1,1)
				glDrawElementsui(GL_TRIANGLE_FAN, cindices)
				if qooim: glDisable(qooim.target)
	
				glPopMatrix()
		glPopMatrix()
	glPopMatrix()
		


	#video.draw()
	#spotlight.draw()
	
	glFinish()
	#window.flip()
	#window.flip()
	drawstopped = True
	

	
def update(dt):	
	pass
	#spotlight.update(dt)
	#print(dt, pyglet.clock.get_fps())
	#game.update(dt)
	
depthim = []
from Queue import Queue
def snapshot():
	queue = Queue()
	pyglet.clock.schedule_once(_snapshot,0.0,queue)
	queue.get()

def _snapshot(dt, queue):
	global depthim
	try:
		depthim = glReadPixels(0, 0, width, height, GL_DEPTH_COMPONENT, GL_FLOAT)
		depthim = depthim[::-1,:]
	finally:
		queue.put('ok')
		
def stop():
	global drawstopped
	drawstopped = True

def refresh():
	global drawstopped
	drawstopped = False
	
try: qooim == '' 
except: qooim = None

import os
drawstopped = False
import traceback
from pylab import *
	
if __name__== '__main__' and first_run:
	
	first_run = False
	pyglet.clock.schedule_interval(update, 0.01)
	tasks.main()
	print tasks.taskconfig
	pyreg.browser.start()
	
	pyglet.resource.path = [os.path.realpath(os.curdir)]
	pyglet.resource.reindex()
	qooim = pyglet.resource.image('qoo.jpg')
	
	while 1:
		try:
			pyglet.app.run()
		except Exception as e:
			drawstopped = True
			traceback.print_exc(e)


