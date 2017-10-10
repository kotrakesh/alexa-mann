import config
import requests, json
from classCommonFunc import classCommonFunc
classCommonFunc = classCommonFunc()

class dbc:
    def pastYesterday(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        query = "SELECT sum(current_output*900/1000000) as result  from current_data where city = 'Heidelberg' and curr_timestamp >= curdate()-1 and curr_timestamp <curdate(); "  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchall()
        temp = data
        cursor.close()
        cnx.close()
        return temp

    def pastlastWeek(self):
        print("starting past last week in database access")
        cnx = classCommonFunc.dataBaseConnection()

        cursor = cnx.cursor()
        print("cursor set up")
        query = "SELECT sum(current_output*900/1000000) as result  from current_data where city = 'Heidelberg' and curr_timestamp >= curdate()-7 and curr_timestamp <curdate(); "  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchall()
        print("data stream: " + str(data))
        temp = "{0:.2f}".format(float(data))
        cursor.close()
        cnx.close()
        print("return value :" + str(temp))
        return temp

    def tillNowCurrent(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        query = "SELECT sum(current_output*900/1000000) as result from current_data where curr_timestamp < now() and curr_timestamp >= curdate() and city = 'Heidelberg'; "  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchall()
        temp = data
        cursor.close()
        cnx.close()
        return temp

    def todayAfterCurrent(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        query = "SELECT sum(t1.current_output*10800/1000000) as result from (select * from future_data where city = 'Heidelberg' order by curr_timestamp desc, weather_date asc limit 8) t1;"  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchall()
        temp = data
        cursor.close()
        cnx.close()
        return temp

    def todayWeather(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        query = "SELECT avg(temperature - 273.15) as result from current_data where curr_timestamp < now() and curr_timestamp >= curdate() and city = 'Heidelberg';"  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchall()
        temp = data
        cursor.close()
        cnx.close()
        return temp

    def tomorrowCurrent(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        query = "SELECT sum(t1.current_output*10800/1000000) as result from (select * from future_data where city = 'Heidelberg' and weather_date >= (curdate()+ 1) order by curr_timestamp desc, weather_date asc limit 8) t1;"  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchall()
        temp = data
        cursor.close()
        cnx.close()
        return temp

    def next5DaysCurrent(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        query = "SELECT sum(t1.current_output*10800/1000000) as result from (select * from future_data where city = 'Heidelberg' order by curr_timestamp desc, weather_date asc limit 40) t1;"  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchall()
        temp = data
        cursor.close()
        cnx.close()
        return temp

    def tomorrowWeather(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        query = "SELECT avg(temperature - 273.15) as result from (select * from future_data where city = 'Heidelberg' and weather_date >= (curdate()+ 1) order by curr_timestamp desc, weather_date asc limit 8) t1;"  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchall()
        temp = data
        cursor.close()
        cnx.close()
        return temp

    def Nnext5DaysWeather(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        query = "SELECT avg(temperature - 273.15) as result from (select * from future_data where city = 'Heidelberg' order by curr_timestamp desc, weather_date asc limit 40) t1;"  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchall()
        temp = data
        cursor.close()
        cnx.close()
        return temp

    def currentNow(self):
        query = "SELECT ip from `heroku_c0277ef6294fdf7`.`raspi_ip` WHERE `status`=1 limit 1;"
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        lines = cursor.execute(query)
        datax = cursor.fetchall()
        for row in datax:
            data = row
        tempip = data[0]
        cursor.close()
        cnx.close()
        url = "http://" + str(tempip) + "/sensordata"
        print(url)
        f = requests.get(url)
        jdata = f.json()
        powq = jdata[0] * config.powerFactor  # actual conversion
        ret = str(powq)
        return ret
