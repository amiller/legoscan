import lego
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
		if not window: raise
	except Exception:
		#pyglet.clock.schedule_interval(video.frameadvance, 0.03)
		create_window()
		first_run = True
		
fps_display = pyglet.clock.ClockDisplay()

@window.event('on_key_press')
def on_key_press(symbol, modifiers):
	if symbol == key.A:
		print 'The "A" key was pressed.'
	elif symbol == key.LEFT:
		print 'The left arrow key was pressed.'
	elif symbol == key.ENTER:
		print 'The enter key was pressed.'
	elif symbol == key.M:
		pass

#@window.event('on_key_press')
def blah(symbol, modifiers):
	print 'blah'
	return False
	
@window.event
def on_mouse_press(x, y, button, modifiers):
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
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
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
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	
	# flush that stack
	try: 
		while 1: glPopMatrix()
	except: pass


	glPushMatrix()
		
	#glMultMatrixf(homoraphy.transpose())
	
	def mouse_rotate(xAngle, yAngle, zAngle):
		glRotatef(xAngle, 1.0, 0.0, 0.0);
		glRotatef(yAngle, 0.0, 1.0, 0.0);
		glRotatef(zAngle, 0.0, 0.0, 1.0);
	glTranslate(0, 0,-0.8)
	mouse_rotate(rotangles[0], rotangles[1], 0);
	global rotmat
	rotmat = glGetFloatv(GL_MODELVIEW_MATRIX)

	glDisable(GL_BLEND)

	# Draw the color pieces
	lego.draw_pieces(tasks.taskconfig.model)
	
	glPopMatrix()
	glFinish()
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
from pylab import imshow, figure
	
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
		except (Exception, KeyboardInterrupt) as e:
			drawstopped = True
			traceback.print_exc(e)
		else:
			if window:
				# Exit
				break


