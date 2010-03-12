import pyglet

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
        print 'Left Mouse: ', x, y

@window.event
def on_resize(width,height):
	glViewport(0,0,width,height)

clearcolor = [0,0,0,0]
@window.event
def on_draw():
	glClearColor(*clearcolor)
	window.clear()
	#game.draw()
	glFinish()
	#window.flip()
	
def update(dt):
	#print(dt, pyglet.clock.get_fps())
	pass
	#game.update(dt)

	
pyglet.clock.schedule_interval(update, 0.01)

#import cProfile
#cProfile.run('pyglet.app.run()','prof')

from IPython.Shell import IPShellEmbed
import sys
ipshell = IPShellEmbed(sys.argv[1:], user_ns = globals())
import threading
def run():
	ipshell()
	pyglet.app.exit()
ipthread = threading.Thread(target=run)
ipthread.start()

pyglet.app.run()
ipthread.join()
sys.exit()
