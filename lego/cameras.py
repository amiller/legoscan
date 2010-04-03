from camera import camcap
import time
import pyreg
import thread
from helpful import *

from uvcobjc import UVCCameraControl

#control = UVCCameraControl.alloc().initWithVendorID_productID_(0x04f2, 0xa13c)

cameras = []
controllers = []

def refresh_cameras():
	global cameras, controllers
	cameras = None
	cameras = [camcap.CamCap()]
	
	controllers = [UVCCameraControl.alloc().initWithLocationID_(0x26200000)]
	controllers[0].setAutoExposure_(0)
	controllers[0].setExposure_(0.95)
	
def set_exposure(val):
	controllers[0].setExposure_(val)
	
def start_thread(camera):
	def go():
		while True:
			image = camera.grabframe()
			if image:
				pyreg.writeimage('img#camera', image)
			time.sleep(0.06)
	thread.start_new(go, ())
	
refresh_cameras()

if cameras[0]:
	start_thread(cameras[0])