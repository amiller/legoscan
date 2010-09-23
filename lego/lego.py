import numpy as np
from opencv.cv import *
from opencv.adaptors import *

from OpenGL.GL import *
from OpenGL.GLU import *


# Takes an array of src points and dst points, returns a homography
# you can load (transposed) into glLoadMatrixf(_.transpose())
def make_homography(src, dst):
	src = src.astype(np.float32)
	dst = dst.astype(np.float32)
	src = np.concatenate((src, np.ones((4,1))), 1)
	dst = np.concatenate((dst, np.ones((4,1))), 1)
	
	_, mat = cvFindHomography(NumPy2Ipl(src), NumPy2Ipl(dst))
	homography = Ipl2NumPy(mat)
	
	homo = np.eye(4)
	homo[:2,:2] = homography[:2,:2]
	homo[3,:2] = homography[2,:2]
	homo[:2,3] = homography[:2,2]
	return homo


def draw_pieces(pieces):

	for piece in pieces:
		glPushMatrix()
		glScale(.05, .05, .07);
		glTranslate(piece.location[0],piece.location[1],piece.location[2])
		glColor(*piece.color)
		glEnableClientState(GL_VERTEX_ARRAY)
		#glEnableClientState(GL_TEXTURE_COORD_ARRAY)
		global cp, indices
		
		# Draw cube
		vertices = [[0, 0, 1], [1, 0, 1],	[0, 1, 1],	[1, 1, 1],
								[0, 0, 0], [1, 0, 0],	[0, 1, 0],	[1, 1, 0]];
								
		# Indices for triangle strip around the cube
		glVertexPointers(vertices);
		indices = [0, 1, 2, 3, 7, 1, 5, 4, 7, 6, 2, 4, 0, 1]
		
		glPushMatrix()
		glScale(piece.shape[0], piece.shape[1], 1)
		glDrawElementsui(GL_TRIANGLE_STRIP, indices)
		glPopMatrix()
		
		# Circles for the little nubs
		h = np.arange(0,2*np.pi+0.1,0.5)
		h = np.hstack((h, [0]))
		cp = np.hstack((np.vstack((np.cos(h), np.sin(h), h*0)),
									  np.vstack((np.cos(h), np.sin(h), h*0+1))))
	
		cp = cp.transpose()
		glVertexPointerf(cp)
		
		radius = 0.32
		# outside indices
		indices = np.vstack((range(len(h)), len(h)+np.arange(len(h))))
		indices = indices.transpose().flatten()
		# circle indices
		cindices = range(len(h), len(h)+len(h))
		
		glPopMatrix(); continue
		
		glColor(np.array(piece.color)*0.8)
		for x in range(piece.shape[0]):
			for y in range(piece.shape[1]):
				glPushMatrix()
				glTranslate(x+0.5, y+0.5, 1)
				glScale(radius, radius, 0.2)
				
				glDrawElementsui(GL_TRIANGLE_STRIP, indices)
				glDrawElementsui(GL_TRIANGLE_FAN, cindices)
	
				glPopMatrix()
		glPopMatrix()