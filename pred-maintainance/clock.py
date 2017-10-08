from apscheduler.schedulers.blocking import BlockingScheduler
import curcomplete
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
	curcomplete.curcomplete()
	print('This job is run every 15 minutes.')

sched.start()