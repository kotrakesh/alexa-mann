from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=15)
def timed_job():
    print('This job is run every 15 minutes.')

sched.start()