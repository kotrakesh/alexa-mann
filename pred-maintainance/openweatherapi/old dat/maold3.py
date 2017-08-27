
import json
import urllib2
import MySQLdb

db = MySQLdb.connect(host="eu-cdbr-west-01.cleardb.com",
                     user="b3465148a734be",
                     passwd="a2c4eda1",
                     db="heroku_c0277ef6294fdf7")


cur = db.cursor()
sqlinsert0 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'broken clouds', "  + str(18.9 + 273.15) + ", " + str(18.1 + 273.15) + ", " + str(19.4 + 273.15) + ", 85 , 1.97 , 1503549000 , 1503599100, '2017-08-24 00:00:00' )"
sqlinsert1 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(24.2 + 273.15) + ", " + str(18.8 + 273.15) + ", " + str(26.2 + 273.15) + ", 71 , 1.48 , 1503549000 , 1503599100, '2017-08-24 06:00:00' )"
sqlinsert2 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(25.9 + 273.15) + ", " + str(25.5 + 273.15) + ", " + str(26.6 + 273.15) + ",  42, 1.82 , 1503549000 , 1503599100, '2017-08-24 12:00:00' )"
sqlinsert3 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'broken clouds', "  + str(24.0 + 273.15) + ", " + str(22.7 + 273.15) + ", " + str(25.0 + 273.15) + ", 41 , 1.23 , 1503549000 , 1503599100, '2017-08-24 18:00:00' )"
sqlinsert44 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'scattered clouds', "  + str(17.2 + 273.15) + ", " + str(17.2 + 273.15) + ", " + str(17.3 + 273.15) + ", 81 , 0.92 , 1503635460 , 1503685380, '2017-08-25 00:00:00' )"
sqlinsert4 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(21.3 + 273.15) + ", " + str(18.4 + 273.15) + ", " + str(25.4 + 273.15) + ", 71 , 1.55 , 1503635460 , 1503685380, '2017-08-25 06:00:00' )"
sqlinsert5 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(27.0 + 273.15) + ", " + str(25.7 + 273.15) + ", " + str(28.8 + 273.15) + ", 62 , 4.37 , 1503635460 , 1503685380, '2017-08-25 12:00:00' )"
sqlinsert6 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(24.2 + 273.15) + ", " + str(22.4 + 273.15) + ", " + str(25.7 + 273.15) + ", 68 , 5.01 , 1503635460 , 1503685380, '2017-08-25 18:00:00' )"
sqlinsert77 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(16.9 + 273.15) + ", " + str(16.3 + 273.15) + ", " + str(17.2 + 273.15) + ", 71 , 0.47 , 1503721980 , 1503771660, '2017-08-26 00:00:00' )"
sqlinsert7 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(25.0 + 273.15) + ", " + str(20.0 + 273.15) + ", " + str(25.0 + 273.15) + ", 85 , 1.82 , 1503721980 , 1503771660, '2017-08-26 06:00:00' )"
sqlinsert8 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(29.5 + 273.15) + ", " + str(26.0 + 273.15) + ", " + str(29.7 + 273.15) + ", 55 , 3.00 , 1503721980 , 1503771660, '2017-08-26 12:00:00' )"
sqlinsert9 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'clear sky', "  + str(28.0 + 273.15) + ", " + str(24.7 + 273.15) + ", " + str(30.0 + 273.15) + ", 40 , 2.52 , 1503721980 , 1503771660, '2017-08-26 18:00:00' )"
sqlinsert10 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'broken clouds', "  + str(15.0 + 273.15) + ", " + str(14.1 + 273.15) + ", " + str(16.9 + 273.15) + ", 71 , 1.85 , 1503808517 , 1503857920, '2017-08-27 00:00:00' )"
sqlinsert11 = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, curr_timestamp ) values ('8.47', '49.49', 'Mannheim', 'broken clouds', "  + str(20.2 + 273.15) + ", " + str(18.3 + 273.15) + ", " + str(22.4 + 273.15) + ", 64 , 0.25 , 1503808517 , 1503857920, '2017-08-27 06:00:00' )"

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
    cur.execute(sqlinsert10)
    cur.execute(sqlinsert11)


except (MySQLdb.Error, MySQLdb.Warning) as e:
    print(e)
cur.execute("commit;")

cur.execute("SELECT * FROM current_data")

rows = cur.fetchall()

for row in rows:
    print(row)