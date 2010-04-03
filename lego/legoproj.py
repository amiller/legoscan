import pyglet
import Image
import bunch
import simplejson as json
from helpful import shell
from lego import *
import spotlight

platform = pyglet.window.get_platform()
display = platform.get_default_display()

# Try to pick the screen that corresponds to the projector
screen = None
for s in display.get_screens():
	if s.width == 2400 and s.height == 600:
		screen = s
		break

# Create the pyglet window including opengl context
from pyglet.window import Window

if not screen:
	screen = display.get_default_screen()
	print("Couldn't find a screen")
	window = Window()
else:
	window = Window(fullscreen=True,screen=screen)

# Bind some events for pyglet's event loop
from pyglet.window import key
from pyglet.window import mouse
from OpenGL.GL import *

fps_display = pyglet.clock.ClockDisplay()

@window.event
def on_key_press(symbol, modifiers):
	if symbol == key.A:
		print 'The "A" key was pressed.'
	elif symbol == key.LEFT:
		print 'The left arrow key was pressed.'
	elif symbol == key.ENTER:
		print 'The enter key was pressed.'
		
@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
			print '[%d, %d],' % (x, y)

@window.event
def on_resize(width_,height_):
	global width, height
	width, height = width_, height_
	glViewport(0,0,width,height)

clearcolor = [0,0,0,0]
@window.event
def on_draw():
	glClearColor(*clearcolor)
	window.clear()
	#game.draw()
	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0,width,0,height,0,20)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	global homo
	glColor(1,1,1)
	glEnable(GL_TEXTURE_RECTANGLE_ARB)
	glPushMatrix()
	if draw1:
		glLoadMatrixf(homography.transpose())
		glBegin(GL_QUADS)
		glTexCoord(0,288), glVertex(0,0,0);
		glTexCoord(0,0), glVertex(0,1,0)
		glTexCoord(352,0), glVertex(1,1,0)
		glTexCoord(352,288), glVertex(1,0,0)
		glEnd()
	
	if draw2:
		glLoadMatrixf(homography2.transpose())
		glBegin(GL_QUADS)
		glTexCoord(0,288), glVertex(0,0,0);
		glTexCoord(0,0), glVertex(0,1,0)
		glTexCoord(352,0), glVertex(1,1,0)
		glTexCoord(352,288), glVertex(1,0,0)
		glEnd()
	
	glDisable(GL_TEXTURE_RECTANGLE_ARB)
	glPopMatrix()
	
	if drawspotlight:
		spotlight.draw()
	
	glFinish()
	#window.flip()
	
import threading
framenum = 0
curstep = 0
playing = False
framelock = threading.Lock()
draw1 = False
draw2 = False
drawspotlight = True
def frameadvance(dt):
	global framenum, playing
	with framelock:
		if framenum >= taskconfig.steps[curstep].clip.end:
			playing = False
		if not playing:
			return
		img = Image.open(framelist[framenum])
		framenum += 1
	glBindTexture(GL_TEXTURE_RECTANGLE_ARB, frametex)
	glTexSubImage2D(GL_TEXTURE_RECTANGLE_ARB, 0, 0, 0, 352, 288, GL_RGB, GL_UNSIGNED_BYTE, img.tostring())
		
def stop():
	# Get the last frame to be put in the buffer
	global framenum, playing
	with framelock:
		framenum = taskconfig.steps[curstep].clip.end-1
		playing = True

def play():
	global framenum, playing
	with framelock:
		framenum = taskconfig.steps[curstep].clip.start
		playing = True

	
def update(dt):	
	pass
	#print(dt, pyglet.clock.get_fps())
	#game.update(dt)

pyglet.clock.schedule_interval(frameadvance, 0.03)
pyglet.clock.schedule_interval(update, 0.01)

#import cProfile
#cProfile.run('pyglet.app.run()','prof')

import numpy as np

def setup():
	global frametex
	frametex = glGenTextures(1)
	for f in [frametex]:
		glBindTexture(GL_TEXTURE_RECTANGLE_ARB, f)
		glTexParameter(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_WRAP_S, GL_CLAMP)
		glTexParameter(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_WRAP_T, GL_CLAMP)
		glTexImage2D(GL_TEXTURE_RECTANGLE_ARB, 0, GL_RGB, 352, 288, 0, GL_RGB, GL_UNSIGNED_BYTE, 
			np.zeros((352,288)))

def find_homography():
	src = np.array([[0, 1],[0, 0],[1, 0],[1, 1]])

	dst = np.array(config['videobox'])
	global homography
	homography = make_homography(src, dst)

	dst = np.array(config['videobox2'])
	global homography2
	homography2 = make_homography(src, dst)
	
	
	
	
def read_projconfig():
	global config
	with open('data/config.js', 'r') as f:
		config = bunch.bunchify(json.load(f))

from IPython.Shell import IPShellEmbed
import sys
ipshell = IPShellEmbed(sys.argv[1:], user_ns = globals())

def run():
	ipshell()
	pyglet.app.exit()
	
	
if __name__ == "__main__":
	ipthread = threading.Thread(target=run)
	ipthread.start()

	setup()
	read_projconfig()
	find_homography()
	spotlight.loadconfig(config)
	stop()

	pyglet.app.run()
	ipthread.join()
	sys.exit()
