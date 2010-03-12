import subprocess
import simplejson as json
from helpful import *
import pyreg

task = None
taskpath = None

def read_config():
	global config
	with open('%s/task.js' % (taskpath,), 'r') as f:
		config = json.load(f)

def choose_task(task_):
	global task, taskpath
	task = task_
	taskpath = "data/tasks/%s" % (task,)
	print 'switched: ', taskpath
	read_config()
	pyreg.push('refresh_task()')

	
def get_frame_list():
	return shell('ls %s/frames/*.jpg' % (taskpath,))

	
def main():
	choose_task('blackship')
	
main()