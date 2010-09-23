import numpy as np

## Functions supporting exponential map representation
# i.e., rodrigues in TOOLBOX_calib

def axis2rot(axis):
	# Return the rotation matrix for this axis-angle/expmap
	h = np.sqrt(np.sum(axis**2))
	axis = axis / h
	s,c = np.sin(h), np.cos(h)
	ux,uy,uz = axis
	R = np.array([
		[ux*ux+(1-ux*ux)*c,  ux*uy*(1-c)-uz*s,  ux*uz*(1-c)+uy*s],
		[ux*uy*(1-c)+uz*s,   uy*uy+(1-uy*uy)*c, uy*uz*(1-c)-ux*s],
		[ux*uz*(1-c)-uy*s,   uz*uy*(1-c)+ux*s,  uz*uz+(1-uz*uz)*c]])
	return R
	
	
### Check
# rot * rot2axis(rot) == rot2axis(rot)
# axis2rot(rot2axis(rot)) == rot
	
def rot2axis(rot):
	# Return the axis angle from this 3x3 rotation matrix
	w,v = np.linalg.eig(rot)
	axis = np.real(v[:,2])
	
	p = np.random.rand(3)
	p = np.cross(p,axis)
	p /= np.sqrt(np.sum(p*p))
	angle = -np.arccos(np.dot(p, np.dot(rot, p)))
	return axis * angle