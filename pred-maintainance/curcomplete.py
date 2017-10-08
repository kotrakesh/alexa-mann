import requests, json
import datetime
import annotate_current
from classCommonFunc import classCommonFunc

classCommonFunc = classCommonFunc()


# fuction curcomplete
def curcomplete():
    cnx = classCommonFunc.dataBaseConnection()
    cur = cnx.cursor()

    now = datetime.datetime.now()
    date_string = now.strftime('%Y-%m-%d %H:%M:%S')

    url = "http://api.openweathermap.org/data/2.5/weather?zip=69115,de&appid=04ac6f7772b575cbd7bb17063a1430f2"
    f = requests.get(url)
    data = f.json()
    sqlinsert = "insert into heroku_c0277ef6294fdf7.current_data (longitude, latitude, city, description, temperature, temperature_min, temperature_max, humidity, wind, sunrise, sunset, current_output, curr_timestamp) values ('" + str(
        data['coord']['lon']) + "', '" + str(data['coord']['lat']) + "', '" + str(data['name']) + "', '" + str(
        data['weather'][0]['description']) + "', " + str(data['main']['temp']) + ", " + str(
        data['main']['temp_min']) + ", " + str(data['main']['temp_max']) + ", " + str(
        data['main']['humidity']) + ", " + str(data['wind']['speed']) + ", " + str(data['sys']['sunrise']) + ", " + str(
        data['sys']['sunset']) + ", " + annotate_current.estimate_current(str(data['weather'][0]['description']),
                                                                          date_string, data['main']['temp'],
                                                                          data['sys']['sunrise'], data['sys'][
                                                                              'sunset']) + ", '" + date_string + "' )"
    try:
        print(sqlinsert)
        r = cur.execute(sqlinsert)
        print(r)
    except (MySQLError) as e:
        print(e)
    cur.execute("commit;")
    cur.close()
    cnx.close()
