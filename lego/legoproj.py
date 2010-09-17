import pyglet
import Image
import bunch
import simplejson as json
from pyreg.helpful import shell
from lego import *
import tasks
import spotlight
import video

config = None

# Set global window to a screen, either the projector or a small one
def create_window():
	global window
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
		#print("Couldn't find a screen")
		window = Window(width=800, height=600)
	else:
		window = Window(fullscreen=True,screen=screen)
try:
	window == ''
except Exception as e:
	create_window()

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
	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(0,width,0,height,0,20)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	video.draw()
	spotlight.draw()
	
	glFinish()
	#window.flip()

	
def update(dt):	
	spotlight.update(dt)
	#print(dt, pyglet.clock.get_fps())
	#game.update(dt)

pyglet.clock.schedule_interval(video.frameadvance, 0.03)
pyglet.clock.schedule_interval(update, 0.01)

#import cProfile
#cProfile.run('pyglet.app.run()','prof')
	
def read_projconfig():
	global config
	with open('data/config.js', 'r') as f:
		config = bunch.bunchify(json.load(f))
	print config


