import config
import requests,json
from sklearn.linear_model import LinearRegression
import numpy as np
import warnings
from classCommonFunc import classCommonFunc
classCommonFunc = classCommonFunc()

class regression:
	def getTrainData(self):
		cnx = classCommonFunc.dataBaseConnection()
		cursor = cnx.cursor()
		query = "SELECT (sunset - sunrise) AS suntime,description, temperature,current_output  FROM `current_data` WHERE current_output>=0 ORDER BY id DESC LIMIT 100" #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		cursor.close()
		cnx.close()
		return data

	def getPrediction(self,x,y,data):
		#
		regressionMdOj = LinearRegression()
		#create training set with old weather data and current data
		regressionMdOj.fit(x,y)
		return regressionMdOj.predict(data)
	def getfurturedata(self):
		cnx = classCommonFunc.dataBaseConnection()
		cursor = cnx.cursor()
		query = "SELECT id,description, temperature FROM `future_data` WHERE current_output=1.00 OR current_output IS NULL LIMIT 700"
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		cursor.close()
		cnx.close()
		return data
	def insertPredictedData(self,id,current):
		cnx = classCommonFunc.dataBaseConnection()
		cursor = cnx.cursor()
		query = "UPDATE `future_data`  SET  current_output ="+str(current)+" WHERE id="+str(id)+""
		ret = cursor.execute(query)
		cnx.commit()
		cursor.close()
		cnx.close()
		return ret	
	def step_gradient(b_current, m_current, points, learningRate):
	    b_gradient = 0
	    m_gradient = 0
	    N = float(len(points))
	    for i in range(0, len(points)):
	        x = points[i, 0]
	        y = points[i, 1]
	        b_gradient += -(2/N) * (y - ((m_current * x) + b_current))
	        m_gradient += -(2/N) * x * (y - ((m_current * x) + b_current))
	    new_b = b_current - (learningRate * b_gradient)
	    new_m = m_current - (learningRate * m_gradient)
	    return [new_b, new_m]

if __name__ == '__main__':
	warnings.filterwarnings("ignore",category=DeprecationWarning)
	r =regression()
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
	#print(xdata)	
	#print(ydata)
	#xdata = np.array(xdata)
	futureArr=r.getfurturedata()
	for i in futureArr:
		wval=1.0
		if (i[1]=='clear sky'):
			wval=4.0
		attr=[i[2],wval]
		#attr = map(float,attr)
		currentPredicted=r.getPrediction(xdata,ydata,attr)
		#print(round(abs(currentPredicted[0]),2))
		print(i[0])
		ret= r.insertPredictedData(i[0],round(abs(currentPredicted[0]),2))
		#print(ret)

