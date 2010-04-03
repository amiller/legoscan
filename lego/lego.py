import numpy as np
from opencv.cv import *
from opencv.adaptors import *

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
