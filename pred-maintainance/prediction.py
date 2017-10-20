import numpy as np
from sklearn import svm
import datetime
from classCommonFunc import classCommonFunc
classCommonFunc = classCommonFunc()

class svcClass:
	def getTrainData(self):
		cnx = classCommonFunc.dataBaseConnection()
		cursor = cnx.cursor()
		query = "SELECT  AS suntime,description, temperature,current_output  FROM `current_data` WHERE current_output>=0 ORDER BY id DESC LIMIT 100" #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		cursor.close()
		cnx.close()
		return data
	def getPrediction(self,data):
		
		listf={"clear sky":0,"broken clouds":1,"scattered clouds":2,"few clouds":3,
		"mist":4,"light intensity drizzle":5,"light intensity shower rain":6,"shower rain":7,
		"light rain":8,"moderate rain":9,"overcast clouds":10,"heavy intensity shower rain":11,
		"fog":12,"thunderstorm":13,"thunderstorm with light rain":14,"light intensity drizzle rain":15,
		"heavy intensity rain":16}
		dataVal=listf[data]
		print(dataVal)
		X = np.array([[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],
			[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16]])
		#X = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
		y = [1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,
			1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0]
		clf = svm.SVC(kernel='rbf', C = 1.0)
		clf.fit(X,y)
		pred = clf.predict([dataVal])
		return pred
	def getfurturedata(self):
		cnx = classCommonFunc.dataBaseConnection()
		cursor = cnx.cursor()
		query = "SELECT description,wind,DATE(weather_date) as wdate FROM `future_data` WHERE  weather_date >= CURDATE() AND weather_date< CURDATE()+6"
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		cursor.close()
		cnx.close()
		return data
	def getfailureprediction(self):
		data= self.getfurturedata()
		failuredate="-"
		failurereason="none"
		for x in data:
			print(x)
			desc = x[0]
			wind = x[1]
			date = x[2]
			predt = self.getPrediction(desc)
			if(predt==[0]):
				failuredate=date.strftime("%d.%m.%Y")
				failurereason = desc+", wind:"+str(wind)+"m/s"
		ret = [failuredate,failurereason]
		return ret
