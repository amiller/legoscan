import subprocess
import simplejson as json
from helpful import *
import pyreg
import bunch
import spotlight

taskname = None
taskpath = None
taskconfig = None

def read_config():
	global taskconfig
	with open('%s/task.js' % (taskpath,), 'r') as f:
		taskconfig = bunch.bunchify(json.load(f))

def choose_task(taskname_):
	global taskname, taskpath
	taskname = taskname_
	taskpath = "data/tasks/%s" % (taskname,)
	print 'switched: ', taskpath
	read_config()
	pyreg.push('refresh_task()')
	global framelist
	framelist = get_frame_list()
	spotlight.loadtask(taskconfig)

	
def get_frame_list():
	return shell('ls %s/frames/*.jpg' % (taskpath,))

	
def main():
	choose_task('blackship')
	
main()