import pyglet
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.framebufferobjects import *
import lego
import tasks
import numpy as np

width = 256
height = 256


def getcontext():
	global window
	try: window.close()
	except: pass
	window = pyglet.window.Window(width=width, height=height)
	
def gentextures():
	global depthtex
	try: glDeleteTextures([depthtex])
	except: pass
	depthtex = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, depthtex)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_DEPTH_TEXTURE_MODE, GL_INTENSITY);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_MODE, GL_COMPARE_R_TO_TEXTURE);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_COMPARE_FUNC, GL_LEQUAL);
	glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT32, width, height, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None);
	
	global fbo
	try: glDeleteFramebuffers([fbo])
	except: pass
	fbo = glGenFramebuffers(1)

	

getcontext()
gentextures()

rotmat = np.array([
[ 0.84804809, -0.20705596,  0.48779327,  0.        ],
[ 0.        ,  0.92050487,  0.39073113,  0.        ],
[-0.52991927, -0.33135879,  0.78063238,  0.        ],
[ 0.        ,  0.        , -0.80000001,  1.        ]])

	
def draw(rotmat):
	
	# Setup framebuffer for depth only drawing
	glBindTexture(GL_TEXTURE_2D, depthtex)
	glBindFramebuffer(GL_FRAMEBUFFER, fbo)
	glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, depthtex, 0)
	glReadBuffer(GL_NONE)
	glDrawBuffer(GL_NONE)
	
	clearcolor = [0,0,0,0]
	glClearColor(*clearcolor)
	glClear(GL_DEPTH_BUFFER_BIT)
	glEnable(GL_DEPTH_TEST)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(60, 1, 0.3,20)
	glMatrixMode(GL_MODELVIEW)
	glLoadMatrixf(rotmat)
	lego.draw_pieces(tasks.taskconfig.model)

	global depthim
	#depthim = glReadPixels(0, 0, width, height, GL_DEPTH_COMPONENT, GL_FLOAT)
	depthim = glGetTexImage(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, GL_FLOAT)
	depthim = depthim[::-1,:]
	
	glBindTexture(GL_TEXTURE_2D, 0)
	glBindFramebuffer(GL_FRAMEBUFFER, 0)
	glDrawBuffer(GL_BACK)
	glReadBuffer(GL_BACK)
	
draw(rotmat)
	