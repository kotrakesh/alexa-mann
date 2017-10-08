from apscheduler.schedulers.blocking import BlockingScheduler
import curcomplete
import fordathd
import regression
sched = BlockingScheduler()

@sched.scheduled_job('cron', minute='*/5')
def timed_job():
	curcomplete.curcomplete()
	print('This job is run every 15 minutes.')
@sched.scheduled_job('cron', hour=15,minute=32)
def scheduled_job():
	fordathd.fordatahd()

	print('This job is run everyday at 5pm.')

sched.start()