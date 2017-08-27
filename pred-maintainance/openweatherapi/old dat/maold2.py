
import json
import urllib2
import MySQLdb

db = MySQLdb.connect(host="eu-cdbr-west-01.cleardb.com",
                     user="b3465148a734be",
                     passwd="a2c4eda1",
                     db="heroku_c0277ef6294fdf7")


cur = db.cursor()
sqlinsert0 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'broken clouds', "  + str(13.7 + 273.15) + ", " + str(13.1 + 273.15) + ", " + str(13.9 + 273.15) + ", 80 , 1.13 , 1503289500 , 1503340260, '2017-08-21 00:00:00' )"
sqlinsert1 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'broken clouds', "  + str(19.9 + 273.15) + ", " + str(15.0 + 273.15) + ", " + str(20.3 + 273.15) + ", 77 , 1.24 , 1503289500 , 1503340260, '2017-08-21 06:00:00' )"
sqlinsert2 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(22.6 + 273.15) + ", " + str(21.2 + 273.15) + ", " + str(23.5 + 273.15) + ", 56 , 1.09 , 1503289500 , 1503340260, '2017-08-21 12:00:00' )"
sqlinsert3 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'broken clouds', "  + str(20.4 + 273.15) + ", " + str(20.1 + 273.15) + ", " + str(22.0 + 273.15) + ", 45 , 1.20 , 1503289500 , 1503340260, '2017-08-21 18:00:00' )"
sqlinsert44 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'broken clouds', "  + str(11.7 + 273.15) + ", " + str(11.0 + 273.15) + ", " + str(12.0 + 273.15) + ", 94 , 0.21 , 1503376020 , 1503426540, '2017-08-22 00:00:00' )"
sqlinsert4 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(16.4 + 273.15) + ", " + str(13.3 + 273.15) + ", " + str(23.0 + 273.15) + ", 78 , 1.67 , 1503376020 , 1503426540, '2017-08-22 06:00:00' )"
sqlinsert5 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(25.0 + 273.15) + ", " + str(22.4 + 273.15) + ", " + str(25.6 + 273.15) + ",60 , 2.07 , 1503376020 , 1503426540, '2017-08-22 12:00:00' )"
sqlinsert6 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(23.4 + 273.15) + ", " + str(21.1 + 273.15) + ", " + str(24.5 + 273.15) + ", 55 , 2.52 , 1503376020 , 1503426540, '2017-08-22 18:00:00' )"
sqlinsert77 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(15.2 + 273.15) + ", " + str(15.0 + 273.15) + ", " + str(15.6 + 273.15) + ", 81 , 0.55 , 1503462480 , 1503512820, '2017-08-23 00:00:00' )"
sqlinsert7 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'scattered clouds', "  + str(23.2 + 273.15) + ", " + str(16.9 + 273.15) + ", " + str(25.8 + 273.15) + ", 60 , 1.35 , 1503462480 , 1503512820, '2017-08-23 06:00:00' )"
sqlinsert8 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(28.4 + 273.15) + ", " + str(24.6 + 273.15) + ", " + str(29.5 + 273.15) + ", 37 , 2.22 , 1503462480 , 1503512820, '2017-08-23 12:00:00' )"
sqlinsert9 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(26.9 + 273.15) + ", " + str(20.7 + 273.15) + ", " + str(28.8 + 273.15) + ", 45 , 0.59 , 1503462480 , 1503512820, '2017-08-23 18:00:00' )"
try:
    cur.execute(sqlinsert0)
    cur.execute(sqlinsert1)
    cur.execute(sqlinsert2)
    cur.execute(sqlinsert3)
    cur.execute(sqlinsert4)
    cur.execute(sqlinsert44)
    cur.execute(sqlinsert5)
    cur.execute(sqlinsert6)
    cur.execute(sqlinsert7)
    cur.execute(sqlinsert77)
    cur.execute(sqlinsert8)
    cur.execute(sqlinsert9)

except (MySQLdb.Error, MySQLdb.Warning) as e:
    print(e)
cur.execute("commit;")

cur.execute("SELECT * FROM current_data")

rows = cur.fetchall()

for row in rows:
    print(row)