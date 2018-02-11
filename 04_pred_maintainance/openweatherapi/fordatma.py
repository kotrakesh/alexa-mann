
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
date_string = now.strftime('%Y-%m-%d %H:%M:%S')#Convert a tuple to a string as specified by the format argument



url = "http://api.openweathermap.org/data/2.5/forecast?zip=68159,de&appid=3a80fa2fe42d112fea2f90eba90a1e52"
data = json.load(urllib2.urlopen(url))

for x in range(0, 39):


    sqlinsert = "insert into heroku_c0277ef6294fdf7.future_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, curr_timestamp, weather_date) values ('" + str(
        data['city']['coord']['lon']) + "', '" + str(data['city']['coord']['lat']) + "', '" + str(data['city']['name']) + "', '" + str(
        data['list'][x]['weather'][0]['description']) + "', " + str(data['list'][x]['main']['temp']) + ", " + str(
        data['list'][x]['main']['temp_min']) + ", " + str(data['list'][x]['main']['temp_max']) + ", " + str(
        data['list'][x]['main']['humidity']) + ", " + str(data['list'][x]['wind']['speed']) + ", '" + date_string + "', '" + str(
        data['list'][x]['dt_txt']) +"')"

    try:
        cur.execute(sqlinsert)

    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
    cur.execute("commit;")

cur.execute("SELECT * FROM future_data")

rows = cur.fetchall()

for row in rows:
    print(row)