import config
import requests,json
from classCommonFunc import classCommonFunc
classCommonFunc = classCommonFunc()

class dbc:
	def pastYesterday(self):
		cnx = classCommonFunc.dataBaseConnection()
		query = "SELECT sum(current_output*900) as result  from current_data where city = 'Heidelberg' and curr_timestamp >= curdate()-1 and curr_timestamp <curdate() " #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		temp=data['result']
		cursor.close()
		return temp
	def pastlastWeek(self):
		cnx = classCommonFunc.dataBaseConnection()
		query = "SELECT sum(current_output*900) as result  from current_data where city = 'Heidelberg' and curr_timestamp >= curdate()-7 and curr_timestamp <curdate() " #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		temp=data['result']
		cursor.close()
		return temp
	def tillNowCurrent(self):
		cnx = classCommonFunc.dataBaseConnection()
		query = "SELECT sum(current_output*900) as result from current_data where curr_timestamp < now() and curr_timestamp >= curdate() and city = 'Heidelberg' " #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		temp=data['result']
		cursor.close()
		return temp
	def todayAfterCurrent(self):
		cnx = classCommonFunc.dataBaseConnection()
		query = "SELECT sum(t1.current_output*10800) as result from (select * from future_data where city = 'Heidelberg' order by curr_timestamp desc, weather_date asc limit :sunglasses: t1" #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		temp=data['result']
		cursor.close()
		return temp
	def todayWeather(self):
		cnx = classCommonFunc.dataBaseConnection()
		query = "SELECT avg(temperature - 273.15) as result from current_data where curr_timestamp < now() and curr_timestamp >= curdate() and city = 'Heidelberg'" #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		temp=data['result']
		cursor.close()
		return temp
	def tomorrowCurrent(self):
		cnx = classCommonFunc.dataBaseConnection()
		query = "SELECT sum(t1.current_output*10800) as result from (select * from future_data where city = 'Heidelberg' and weather_date >= (curdate()+ 1) order by curr_timestamp desc, weather_date asc limit :sunglasses: t1" #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		temp=data['result']
		cursor.close()
		return temp
	def next5DaysCurrent(self):
		cnx = classCommonFunc.dataBaseConnection()
		query = "SELECT sum(t1.current_output*10800) as result from (select * from future_data where city = 'Heidelberg' order by curr_timestamp desc, weather_date asc limit 40) t1" #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		temp=data['result']
		cursor.close()
		return temp
	def tomorrowWeather(self):
		cnx = classCommonFunc.dataBaseConnection()
		query = "SELECT avg(temperature - 273.15) as result from (select * from future_data where city = 'Heidelberg' and weather_date >= (curdate()+ 1) order by curr_timestamp desc, weather_date asc limit :sunglasses: t1" #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		temp=data['result']
		cursor.close()
		return temp
	def Nnext5DaysWeather(self):
		cnx = classCommonFunc.dataBaseConnection()
		query = "SELECT avg(temperature - 273.15) as result from (select * from future_data where city = 'Heidelberg' order by curr_timestamp desc, weather_date asc limit 40) t1" #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		temp=data['result']
		cursor.close()
		return temp
	def currentNow(self):
		query = "SELECT ip from `heroku_c0277ef6294fdf7`.`raspi_ip` WHERE `status`=1 limit 1";
		cnx = classCommonFunc.dataBaseConnection()
		x = cnx.cursor()
		x.execute(query)
		for row in x:
			data = row
		tempip=data[0]
		cnx.close()
		url = "http://" +str(tempip)+ "/sensordata"
		print(url)
		f = requests.get(url)
		jdata= f.json()
		powq = (jdata[0] * jdata[1])+jdata[0]#actual conversion	
		ret = str(powq)		
		return ret