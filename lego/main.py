import pyreg
import legoproj
import tasks
import video
if __name__ == "__main__":
	
	legoproj.read_projconfig()
	from legoproj import *
	
	tasks.main()
	
	print tasks.taskconfig
	spotlight.loadconfig(config)
	
	video.setup()
	video.find_homography()
	video.stop()
	
	pyreg.browser.start()
	pyglet.app.run()

