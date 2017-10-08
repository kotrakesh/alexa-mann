import requests,json
import datetime
from classCommonFunc import classCommonFunc
classCommonFunc = classCommonFunc()


def fordatahd():

    cnx = classCommonFunc.dataBaseConnection()
    cur = cnx.cursor()

    now = datetime.datetime.now()
    date_string = now.strftime('%Y-%m-%d %H:%M:%S')



    url = "http://api.openweathermap.org/data/2.5/forecast?zip=69115,de&appid=3a80fa2fe42d112fea2f90eba90a1e52"
    f = requests.get(url)
    data = f.json()

    for x in range(0, 39):


        sqlinsert = "insert into heroku_c0277ef6294fdf7.future_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, curr_timestamp, weather_date) values ('" + str(
            data['city']['coord']['lon']) + "', '" + str(data['city']['coord']['lat']) + "', '" + str(data['city']['name']) + "', '" + str(
            data['list'][x]['weather'][0]['description']) + "', " + str(data['list'][x]['main']['temp']) + ", " + str(
            data['list'][x]['main']['temp_min']) + ", " + str(data['list'][x]['main']['temp_max']) + ", " + str(
            data['list'][x]['main']['humidity']) + ", " + str(data['list'][x]['wind']['speed']) + ", '" + date_string + "', '" + str(
            data['list'][x]['dt_txt']) +"')"

        try:
            cur.execute(sqlinsert)

        except (MySQLError, MySQLWarning) as e:
            print(e)
        cur.execute("commit;")

    cur.execute("SELECT * FROM future_data")

    rows = cur.fetchall()

    for row in rows:
        print(row)