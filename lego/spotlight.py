from lego import *
import numpy as np
from OpenGL.GL import *

# Read the drawing field and dimensions from the config
# Prepare homographies, build into opengl

# Start with the base layer, all the pieces on the ground layer

# For each subsequent piece
# - Show the right size color and orientation to the side
# - Spotlight the location where it goes
# - Animate some motion in between (optional?)


layer = 0
piece = 0
homography = []
taskconfig = {}
drawpieces = []
spotpieces = []
remainingpieces = []

def loadtask(taskconfig_):
	global taskconfig
	taskconfig = taskconfig_
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
		remainingpieces = [x for x in taskconfig.model if x.location[2] > 0]
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
	drawpieces = [x for x in taskconfig.model if x.location[2] == 0]
	spotpieces = []
	remainingpieces = []
	
def draw():
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
	
	# Draw the 