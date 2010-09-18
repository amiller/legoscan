import numpy as np
from OpenGL.GL import *
import legoproj
import lego
import tasks
from PIL import Image

draw1 = False
draw2 = False

import threading
framenum = 0
curstep = 0
playing = False
framelock = threading.Lock()

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

	dst = np.array(legoproj.config['videobox'])
	global homography
	homography = lego.make_homography(src, dst)

	dst = np.array(legoproj.config['videobox2'])
	global homography2
	homography2 = lego.make_homography(src, dst)
	
def frameadvance(dt):
	global framenum, playing
	with framelock:
		if framenum >= tasks.taskconfig.steps[curstep].clip.end:
			playing = False
		if not playing:
			return
		img = Image.open(tasks.framelist[framenum])
		framenum += 1
	glBindTexture(GL_TEXTURE_RECTANGLE_ARB, frametex)
	glTexSubImage2D(GL_TEXTURE_RECTANGLE_ARB, 0, 0, 0, 352, 288, GL_RGB, GL_UNSIGNED_BYTE, img.tostring())
	
def stop():
	# Get the last frame to be put in the buffer
	global framenum, playing
	with framelock:
		framenum = tasks.taskconfig.steps[curstep].clip.end-1
		playing = True

def play():
	global framenum, playing
	with framelock:
		framenum = tasks.taskconfig.steps[curstep].clip.start
		playing = True
		
def draw():
	
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
	