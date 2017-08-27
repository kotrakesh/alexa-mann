
import json
import urllib2
import MySQLdb

db = MySQLdb.connect(host="eu-cdbr-west-01.cleardb.com",
                     user="b3465148a734be",
                     passwd="a2c4eda1",
                     db="heroku_c0277ef6294fdf7")


cur = db.cursor()

sqlinsert1 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'broken clouds', "  + str(20.4 + 273.15) + ", " + str(19.1 + 273.15) + ", " + str(24.9 + 273.15) + ", 84 , 1.93 , 1503030060 , 1503081420, '2017-08-18 06:00:00' )"
sqlinsert2 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(26.2 + 273.15) + ", " + str(21.0 + 273.15) + ", " + str(26.4 + 273.15) + ", 62 , 4.74 , 1503030060 , 1503081420, '2017-08-18 12:00:00' )"
sqlinsert3 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'scattered clouds', "  + str(19.7 + 273.15) + ", " + str(18.0 + 273.15) + ", " + str(21.6 + 273.15) + ", 83 , 2.21 , 1503030060 , 1503081420, '2017-08-18 18:00:00' )"
sqlinsert4 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'broken clouds', "  + str(14.5 + 273.15) + ", " + str(14.3 + 273.15) + ", " + str(19.7 + 273.15) + ", 80 , 3.01 , 1503116580 , 1503167700, '2017-08-19 06:00:00' )"
sqlinsert5 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'broken clouds', "  + str(20.7 + 273.15) + ", " + str(19.4 + 273.15) + ", " + str(22.2 + 273.15) + ", 69 , 3.42 , 1503116580 , 1503167700, '2017-08-19 12:00:00' )"
sqlinsert6 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'scattered clouds', "  + str(20.4 + 273.15) + ", " + str(19.1 + 273.15) + ", " + str(21.5 + 273.15) + ", 39 , 2.32 , 1503116580 , 1503167700, '2017-08-19 18:00:00' )"
sqlinsert7 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'broken clouds', "  + str(17.2 + 273.15) + ", " + str(15.0 + 273.15) + ", " + str(19.6 + 273.15) + ", 63 , 2.15 , 1503203040 , 1503253980, '2017-08-20 06:00:00' )"
sqlinsert8 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(21.0 + 273.15) + ", " + str(20.7 + 273.15) + ", " + str(21.9 + 273.15) + ", 47 , 4.73 , 1503203040 , 1503253980, '2017-08-20 12:00:00' )"
sqlinsert9 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(19.9 + 273.15) + ", " + str(20.0 + 273.15) + ", " + str(20.3 + 273.15) + ", 55 , 4.29 , 1503203040 , 1503253980, '2017-08-20 18:00:00' )"
try:
    cur.execute(sqlinsert1)
    cur.execute(sqlinsert2)
    cur.execute(sqlinsert3)
    cur.execute(sqlinsert4)
    cur.execute(sqlinsert5)
    cur.execute(sqlinsert6)
    cur.execute(sqlinsert7)
    cur.execute(sqlinsert8)
    cur.execute(sqlinsert9)

except (MySQLdb.Error, MySQLdb.Warning) as e:
    print(e)
cur.execute("commit;")

cur.execute("SELECT * FROM current_data")

rows = cur.fetchall()

for row in rows:
    print(row)