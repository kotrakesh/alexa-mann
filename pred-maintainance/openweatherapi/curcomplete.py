
import json
import urllib2
import MySQLdb
import datetime


db = MySQLdb.connect(host="eu-cdbr-west-01.cleardb.com",
                     user="b3465148a734be",
                     passwd="a2c4eda1",
                     db="heroku_c0277ef6294fdf7")


cur = db.cursor()

now = datetime.datetime.now()
date_string = now.strftime('%Y-%m-%d %H:%M:%S')



url = "http://api.openweathermap.org/data/2.5/weather?zip=69115,de&appid=04ac6f7772b575cbd7bb17063a1430f2"
data = json.load(urllib2.urlopen(url))
sqlinsert = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp) values ('"  + str(data['coord']['lon'])+ "', '" + str(data['coord']['lat']) + "', '"  + str(data['name']) + "', '"  + str(data['weather'][0]['description']) + "', "  + str(data['main']['temp']) + ", "  + str(data['main']['temp_min']) + ", "  + str(data['main']['temp_max']) + ", "  + str(data['main']['humidity']) + ", "  + str(data['wind']['speed']) + ", "  + str(data['sys']['sunrise']) + ", "  + str(data['sys']['sunset']) + ", '" + date_string + "' )"
try:
    cur.execute(sqlinsert)

except (MySQLdb.Error, MySQLdb.Warning) as e:
    print(e)
cur.execute("commit;")

url = "http://api.openweathermap.org/data/2.5/weather?zip=68159,de&appid=3a80fa2fe42d112fea2f90eba90a1e52"

data = json.load(urllib2.urlopen(url))
sqlinsert = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp) values ('"  + str(data['coord']['lon'])+ "', '" + str(data['coord']['lat']) + "', '"  + str(data['name']) + "', '"  + str(data['weather'][0]['description']) + "', "  + str(data['main']['temp']) + ", "  + str(data['main']['temp_min']) + ", "  + str(data['main']['temp_max']) + ", "  + str(data['main']['humidity']) + ", "  + str(data['wind']['speed']) + ", "  + str(data['sys']['sunrise']) + ", "  + str(data['sys']['sunset']) + ", '" + date_string + "' )"
try:
    cur.execute(sqlinsert)

except (MySQLdb.Error, MySQLdb.Warning) as e:
    print(e)
cur.execute("commit;")