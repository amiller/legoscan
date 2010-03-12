from opencv.highgui import *
from opencv.adaptors import *
from uvcobjc import UVCCameraControl
from camera import camcap


usbid = 0x26200000
#control = UVCCameraControl.alloc().initWithLocationID_(usbid)
control = UVCCameraControl.alloc().initWithVendorID_productID_(0x04f2, 0xa13c)
control.setAutoExposure_(0)
control.setExposure_(0.785)
print 'autoexposure:', control.getAutoExposure()

#cvNamedWindow("preview")
#cam = cvCreateCameraCapture(1)
cam = camcap.CamCap()

def run():
	capturing = False
	i = 0

	while True:
		frame = cam.grabframe()
		if not frame: continue
		frame = PIL2Ipl(frame.convert('RGB'))
		cvShowImage("preview", frame)
	
		if capturing:
			i += 1
			name = 'frame_%05d.jpg' % (i)
			cvSaveImage(name, frame)
		
		c = cvWaitKey(10)
		if c == 'c':
			capturing = not capturing
			print 'CAPTURING: ', capturing
			
			