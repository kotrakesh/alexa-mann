
import json
import urllib2
import MySQLdb

db = MySQLdb.connect(host="eu-cdbr-west-01.cleardb.com",
                     user="b3465148a734be",
                     passwd="a2c4eda1",
                     db="heroku_c0277ef6294fdf7")


cur = db.cursor()

sqlinsert1 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.69', '49.41', 'Heidelberg', 'broken clouds', "  + str(20.2 + 273.15) + ", " + str(19.1 + 273.15) + ", " + str(24.9 + 273.15) + ", 94 , 1.94 , 1503030000 , 1503081360, '2017-08-18 06:00:00' )"
sqlinsert2 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.69', '49.41', 'Heidelberg', 'clear sky', "  + str(26.2 + 273.15) + ", " + str(21.2 + 273.15) + ", " + str(27.5 + 273.15) + ", 61 , 4.74 , 1503030000 , 1503081360, '2017-08-18 12:00:00' )"
sqlinsert3 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.69', '49.41', 'Heidelberg', 'broken clouds', "  + str(19.4 + 273.15) + ", " + str(18.1 + 273.15) + ", " + str(21.4 + 273.15) + ", 87 , 2.20 , 1503030000 , 1503081360, '2017-08-18 18:00:00' )"
sqlinsert4 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.69', '49.41', 'Heidelberg', 'broken clouds', "  + str(14.2 + 273.15) + ", " + str(14.3 + 273.15) + ", " + str(19.7 + 273.15) + ", 84 , 2.94 , 1503116520 , 1503167640, '2017-08-19 06:00:00' )"
sqlinsert5 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.69', '49.41', 'Heidelberg', 'broken clouds', "  + str(20.7 + 273.15) + ", " + str(19.4 + 273.15) + ", " + str(22.2 + 273.15) + ", 64 , 3.67 , 1503116520 , 1503167640, '2017-08-19 12:00:00' )"
sqlinsert6 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.69', '49.41', 'Heidelberg', 'broken clouds', "  + str(20.4 + 273.15) + ", " + str(19.1 + 273.15) + ", " + str(21.5 + 273.15) + ", 46 , 2.02 , 1503116520 , 1503167640, '2017-08-19 18:00:00' )"
sqlinsert7 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.69', '49.41', 'Heidelberg', 'broken clouds', "  + str(17.2 + 273.15) + ", " + str(15.0 + 273.15) + ", " + str(19.6 + 273.15) + ", 63 , 2.15 , 1503202980 , 1503253920, '2017-08-20 06:00:00' )"
sqlinsert8 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.69', '49.41', 'Heidelberg', 'clear sky', "  + str(21.4 + 273.15) + ", " + str(20.4 + 273.15) + ", " + str(21.9 + 273.15) + ", 40 , 5.20 , 1503202980 , 1503253920, '2017-08-20 12:00:00' )"
sqlinsert9 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.69', '49.41', 'Heidelberg', 'clear sky', "  + str(19.9 + 273.15) + ", " + str(19.7 + 273.15) + ", " + str(20.3 + 273.15) + ", 42 , 4.63 , 1503202980 , 1503253920, '2017-08-20 18:00:00' )"
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