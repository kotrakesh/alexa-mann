import MySQLdb
from config.py import dataBaseConnection
	
	def pastYesterday(self):
		cursor = global dataBaseConnection()
		query = "SELECT sum(current_output*900) as result  from current_data where city = 'Heidelberg' and curr_timestamp >= curdate()-1 and curr_timestamp <curdate() " #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		temp=data['result']
		cursor.close()
		return temp
	def pastlastWeek(self):
		cursor = global dataBaseConnection()
		query = "SELECT sum(current_output*900) as result  from current_data where city = 'Heidelberg' and curr_timestamp >= curdate()-7 and curr_timestamp <curdate() " #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		temp=data['result']
		cursor.close()
		return temp
	def tillNowCurrent(self):
		cursor = global dataBaseConnection()
		query = "SELECT sum(current_output*900) as result from current_data where curr_timestamp < now() and curr_timestamp >= curdate() and city = 'Heidelberg' " #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		temp=data['result']
		cursor.close()
		return temp
	def todayAfterCurrent(self):
		cursor = global dataBaseConnection()
		query = "SELECT sum(t1.current_output*10800) as result from (select * from future_data where city = 'Heidelberg' order by curr_timestamp desc, weather_date asc limit :sunglasses: t1" #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		temp=data['result']
		cursor.close()
		return temp
	def todayWeather(self):
		cursor = global dataBaseConnection()
		query = "SELECT avg(temperature - 273.15) as result from current_data where curr_timestamp < now() and curr_timestamp >= curdate() and city = 'Heidelberg'" #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		temp=data['result']
		cursor.close()
		return temp
	def tomorrowCurrent(self):
		cursor = global dataBaseConnection()
		query = "SELECT sum(t1.current_output*10800) as result from (select * from future_data where city = 'Heidelberg' and weather_date >= (curdate()+ 1) order by curr_timestamp desc, weather_date asc limit :sunglasses: t1" #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		temp=data['result']
		cursor.close()
		return temp
	def next5DaysCurrent(self):
		cursor = global dataBaseConnection()
		query = "SELECT sum(t1.current_output*10800) as result from (select * from future_data where city = 'Heidelberg' order by curr_timestamp desc, weather_date asc limit 40) t1" #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		temp=data['result']
		cursor.close()
		return temp
	def tomorrowWeather(self):
		cursor = global dataBaseConnection()
		query = "SELECT avg(temperature - 273.15) as result from (select * from future_data where city = 'Heidelberg' and weather_date >= (curdate()+ 1) order by curr_timestamp desc, weather_date asc limit :sunglasses: t1" #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		temp=data['result']
		cursor.close()
		return temp
	def Nnext5DaysWeather(self):
		cursor = global dataBaseConnection()
		query = "SELECT avg(temperature - 273.15) as result from (select * from future_data where city = 'Heidelberg' order by curr_timestamp desc, weather_date asc limit 40) t1" #actual SQL statement to be executed
		lines = cursor.execute(query) #execute the query
		data = cursor.fetchall()
		temp=data['result']
		cursor.close()
		return temp






# ask how are we piontng which metho to call.