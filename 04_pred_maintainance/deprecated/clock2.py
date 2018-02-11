from apscheduler.schedulers.blocking import BlockingScheduler
import curcomplete
import fordathd
import regression
sched = BlockingScheduler()

@sched.scheduled_job('cron', minute='*/15')
def timed_job():
	curcomplete.curcomplete()
	print('This job is run every 15 minutes.')
@sched.scheduled_job('cron', hour=7)
def scheduled_job():
	fordathd.fordatahd()
	print('This job is run everyday at 9am.')
@sched.scheduled_job('cron', hour=7,minute=5)
def scheduled_job():
	r = regression.regression()
	trainArr = r.getTrainData()
	xdata=[]
	ydata =[]
	for i in trainArr:
		if(i[3]!=0.0):
			#print(i)
			wval=1.0
			if (i[1]=='clear sky'):
				wval=4.0
			xdata.append([i[2],wval])
			ydata.append(i[3])
	#xdata = map(float,xdata)
	#ydata = map(float,ydata)	
	print(xdata)	
	print(ydata)
	#xdata = np.array(xdata)
	futureArr=r.getfurturedata()
	for i in futureArr:
		wval=1.0
		if (i[1]=='clear sky'):
			wval=4.0
		attr=[i[2],wval]
		#attr = map(float,attr)
		currentPredicted=r.getPrediction(xdata,ydata,attr)
		print(round(abs(currentPredicted[0]),2))
		print(i[0])
		ret= r.insertPredictedData(i[0],round(abs(currentPredicted[0]),2))
		print(ret)
	print('This job is run everyday at 9:05am.')		
@sched.scheduled_job('cron', hour=16,minute=20)
def scheduled_job_eve():
	fordathd.fordatahd()
	print('This job is run everyday at 9pm.')
@sched.scheduled_job('cron', hour=16,minute=29)
def scheduled_job_eve():
	r = regression.regression()
	trainArr = r.getTrainData()
	xdata=[]
	ydata =[]
	for i in trainArr:
		if(i[3]!=0.0):
			#print(i)
			wval=1.0
			if (i[1]=='clear sky'):
				wval=4.0
			xdata.append([i[2],wval])
			ydata.append(i[3])
	#xdata = map(float,xdata)
	#ydata = map(float,ydata)	
	print(xdata)	
	print(ydata)
	#xdata = np.array(xdata)
	futureArr=r.getfurturedata()
	for i in futureArr:
		wval=1.0
		if (i[1]=='clear sky'):
			wval=4.0
		attr=[i[2],wval]
		#attr = map(float,attr)
		currentPredicted=r.getPrediction(xdata,ydata,attr)
		print(round(abs(currentPredicted[0]),2))
		print(i[0])
		ret= r.insertPredictedData(i[0],round(abs(currentPredicted[0]),2))
		print(ret)
	print('This job is run everyday at 9:05pm.')


sched.start()