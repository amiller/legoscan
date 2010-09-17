from lego import *
import numpy as np
from OpenGL.GL import *
import tasks

# Read the drawing field and dimensions from the config
# Prepare homographies, build into opengl

# Start with the base layer, all the pieces on the ground layer

# For each subsequent piece
# - Show the right size color and orientation to the side
# - Spotlight the location where it goes
# - Animate some motion in between (optional?)

drawspotlight = True
drawcircles = True
layer = 0
piece = 0
homography = []
drawpieces = []
spotpieces = []
remainingpieces = []
counter = 0.0
linefreq = 1	# Line every 2 seconds
linecount = 4
lineradius = 3

def loadtask(taskconfig):
	reset()
	
def loadconfig(config): 
	# pull important stuff out of the config object
	global homography
	homography = make_homography(np.array(config.builddims),
		np.array(config.buildbox))
	print homography

# Go to the next step
def advance():
	global remainingpieces, drawpieces, spotpieces
	global layer, piece
	if layer == 0:
		print 'Advancing Layer'
		layer = 1
		piece = 0
		# Find the next piece that's off the first layer
		remainingpieces = [x for x in tasks.taskconfig.model if x.location[2] > 0]
		spotpieces = [remainingpieces[0]]
		drawpieces = []
	else:
		print 'Advancing Piece %d' % (piece,)
		# Find the next piece
		piece += 1
		if piece < len(remainingpieces):
			spotpieces = [remainingpieces[piece]]
		else:
			reset()

def reset():
	global layer, piece, drawpieces, spotpieces, remainingpieces
	layer = 0
	piece = 0
	drawpieces = [x for x in tasks.taskconfig.model if x.location[2] == 0]
	spotpieces = []
	remainingpieces = []
	
def update(dt):
	global counter
	counter += dt * linefreq
	counter -= np.floor(counter)
	
	
def draw_beatcircles(piece):
	glPushMatrix()
	glColor(*[1,1,1])
	glTranslate(piece.location[0],piece.location[1],0)
	glTranslate(piece.shape[0]/2,piece.shape[1]/2,0)
	def draw_rectangle(scale):
		glPushMatrix()
		glScale(scale,scale,1)
		sx, sy = piece.shape
		glLineWidth(2)
		glBegin(GL_LINE_STRIP)
		glVertex(-sx/2,-sy/2)
		glVertex(-sx/2, sy/2)
		glVertex( sx/2, sy/2)
		glVertex( sx/2,-sy/2)
		glVertex(-sx/2,-sy/2)
		glEnd()
		glPopMatrix()
	for i in range(linecount):
		d = (1.0-counter + float(i)) / linecount
		glColor(1,1,1,1-d)
		draw_rectangle (d*lineradius + 1)
	glPopMatrix()
	
def draw():
	if not drawspotlight: return
	
	# Deal with the homography
	glMatrixMode(GL_MODELVIEW)
	glPushMatrix()
	if layer > 0:
		glTranslate(320,0,0)
		factor = 2.0/480
		glScale(1+factor,1+factor,1)
		glTranslate(-320/(1+factor),0,0)
		
	glMultMatrixf(homography.transpose())
	
	# Draw the color pieces
	for piece in drawpieces:
		glPushMatrix()
		glTranslate(piece.location[0],piece.location[1],0)
		glColor(*piece.color)
		glBegin(GL_QUADS)
		glVertex(0,0)
		glVertex(0,piece.shape[1])
		glVertex(piece.shape[0],piece.shape[1])
		glVertex(piece.shape[0],0)
		glEnd()
		glPopMatrix()
		
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
	
	# Draw the spotlight
	for piece in spotpieces:
		glPushMatrix()
		glColor(*[1,1,1])
		glTranslate(piece.location[0],piece.location[1],0)
		glBegin(GL_QUADS)
		glVertex(0,0)
		glVertex(0,piece.shape[1])
		glVertex(piece.shape[0],piece.shape[1])
		glVertex(piece.shape[0],0)
		glEnd()
		glPopMatrix()
		
		if drawcircles:
			draw_beatcircles(piece)
		
		# Draw to the side
		glPushMatrix()
		glTranslate(piece.location[0]-12,piece.location[1],0)
		glColor(*piece.color)
		glBegin(GL_QUADS)
		glVertex(0,0)
		glVertex(0,piece.shape[1])
		glVertex(piece.shape[0],piece.shape[1])
		glVertex(piece.shape[0],0)
		glEnd()
		glPopMatrix()
	glPopMatrix()
	
	