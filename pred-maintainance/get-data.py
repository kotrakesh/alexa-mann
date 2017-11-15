import json

import mysql.connector
import urllib.request as urllib2

import config


class weatherDataGetter:
	def get_data(self):
		appid='04ac6f7772b575cbd7bb17063a1430f2'
		pincode= '69115,de'
		url='http://api.openweathermap.org/data/2.5/weather?zip='+pincode+'&appid='+appid
		data={}
		req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
		f = urllib2.urlopen(req)
		for x in f:
			data  = json.loads(x)
			#print(data)
		f.close()
		self.lon=str(data['coord']['lon'])
		self.lat=str(data['coord']['lat']) 
		self.description = data['weather'][0]['description']
		self.temperature=str(data['main']['temp'])
		self.temp_min=str(data['main']['temp_min'])
		self.temp_max=str(data['main']['temp_max'])
		self.humidity=str(data['main']['humidity'])
		self.sunrise =str(data['sys']['sunrise'])
		self.sunset =str(data['sys']['sunset'])
		self.wind =str(data['wind']['speed'])
		self.city =data['name']

	def insert_data(self):
		query = "INSERT INTO `heroku_c0277ef6294fdf7`.`weather_data` SET`longitude`= '"+self.lon+"',`latitude`= '"+self.lat+"',`city`= '"+self.city+"',`description`= '"+self.description+"',`temperature`= '"+self.temperature+"',`temperature_min`= '"+self.temp_min+"',`temperature_max`= '"+self.temp_max+"',`humidity`= '"+self.humidity+"',`wind`= '"+self.wind+"',`sunrise`= '"+self.sunrise+"',`sunset`='"+self.sunset+"'"
		#print (query)
		cnx = mysql.connector.connect(user=config.dbUser, password=config.dbPassowrd,
                                      host=config.dbHost,
                                      database=config.dbDatabase)
		x = cnx.cursor()

		x.execute(query)
		cnx.commit()
		cnx.close()

if __name__ == '__main__':
	w =weatherDataGetter()
	w.get_data()
	w.insert_data()