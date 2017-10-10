from apscheduler.schedulers.blocking import BlockingScheduler
import curcomplete
import fordathd
import regression

def curcomp():
	curcomplete.curcomplete()
	print('This job is run every 15 minutes.')

def fordat1():
	fordathd.fordatahd()
	print('This job is run everyday at 9am.')

def reg1():
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

def fordat2():
	fordathd.fordatahd()
	print('This job is run everyday at 9pm.')

def reg2():
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


if __name__ == '__main__':
	sched = BlockingScheduler()
	sched.add_job(curcomp, 'cron', minute='*/15')
	sched.add_job(fordat1, 'cron', hour=7)
	sched.add_job(reg1, 'cron', hour=7,minute=5)
	sched.add_job(fordat2, 'cron', hour=19)
	sched.add_job(reg2, 'cron', hour=19,minute=5)

	sched.start()