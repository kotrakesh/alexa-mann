from apscheduler.schedulers.blocking import BlockingScheduler
import curcomplete
import fordatahd
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=15)
def timed_job():
	curcomplete.curcomplete()
	print('This job is run every 15 minutes.')
@sched.scheduled_job('cron', hour=17)
def scheduled_job():
	fordatahd.fordatahd()
    print('This job is run everyday at 5pm.')

sched.start()
sched.start()