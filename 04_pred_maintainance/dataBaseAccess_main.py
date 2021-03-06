import config
import requests, json, pymysql
from classCommonFunc import classCommonFunc

classCommonFunc = classCommonFunc()

class dbc:
    def pastYesterday(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        #computing total current received yesterday
        query = "SELECT sum(current_output*900/1000000) as result  from current_data where city = 'Heidelberg' and curr_timestamp >= curdate()-1 and curr_timestamp <curdate(); "  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchone()
        temp = float("{0:.2f}".format(float(data[0])))
        cursor.close()
        cnx.close()
        return temp

    def pastlastWeek(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        #computing total current received last week
        query = "SELECT sum(current_output*900/1000000) as result from current_data where city = 'Heidelberg' and curr_timestamp >= curdate()-7 and curr_timestamp <curdate(); "  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchone()
        temp = float("{0:.2f}".format(float(data[0])))
        cursor.close()
        cnx.close()
        return temp

    def tillNowCurrent(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        #computing total current received today till the present time
        query = "SELECT sum(current_output*900/1000000) as result from current_data where curr_timestamp < DATE_ADD(now(), INTERVAL 2 HOUR) and curr_timestamp >= curdate() and city = 'Heidelberg'; "  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchone()
        temp = float("{0:.2f}".format(float(data[0])))
        cursor.close()
        cnx.close()
        return temp

    def todayAfterCurrent(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        #computing expected current after present time
        query = "SELECT sum(t1.current_output*10800/1000000) as result from (select * from future_data where city = 'Heidelberg' order by curr_timestamp desc, weather_date asc limit 8) t1;"  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchone()
        data1 = data[0]
        if data1 is None:
            data1 = 0.0
        temp = float("{0:.2f}".format(float(data1)))
        cursor.close()
        cnx.close()
        return temp

    def nowWeather(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        #receiving details about present weather 
        query = "select description, (temperature - 273.15) as tempo, city from current_data where city = 'Heidelberg' order by id desc limit 1; "  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchone()
        temp = (float("{0:.2f}".format(float(data[1]))), data[0], data[2])
        print(temp)
        cursor.close()
        cnx.close()
        return temp

    def todayWeather(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        #receiving details about today's weather 
        query = "SELECT avg(temperature - 273.15) as result from current_data where curr_timestamp < DATE_ADD(now(), INTERVAL 2 HOUR) and curr_timestamp >= curdate() and city = 'Heidelberg';"  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchone()
        temp = float("{0:.2f}".format(float(data[0])))
        cursor.close()
        cnx.close()
        return temp

    def todayWeatherDesc(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        #receiveing description about today's weather
        query = "SELECT description as result from current_data where city = 'Heidelberg' and curr_timestamp < DATE_ADD(now(), INTERVAL 2 HOUR) and curr_timestamp >= curdate() group by description order by count(description) desc limit 1;"
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchone()
        temp = data[0]
        cursor.close()
        cnx.close()
        return temp

    def tomorrowCurrent(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        #computing expected tomorrow current 
        query = "SELECT sum(t1.current_output*10800/1000000) as result from (select * from future_data where city = 'Heidelberg' and weather_date >= (curdate()+ 1) order by curr_timestamp desc, weather_date asc limit 8) t1;"  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchone()
        data1 = data[0]
        if data1 is None:
            data1 = 0.0
        temp = float("{0:.2f}".format(float(data1)))
        cursor.close()
        cnx.close()
        return temp

    def next5DaysCurrent(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        #computing expected next 5 day's current 
        query = "SELECT sum(t1.current_output*10800/1000000) as result from (select * from future_data where city = 'Heidelberg' order by curr_timestamp desc, weather_date asc limit 40) t1;"  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchone()
        data1 = data[0]
        if data1 is None:
            data1 = 0.0
        temp = float("{0:.2f}".format(float(data1)))
        cursor.close()
        cnx.close()
        return temp

    def tomorrowWeather(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        #receiving details about tomorrow's weather 
        query = "SELECT avg(temperature - 273.15) as result from (select * from future_data where city = 'Heidelberg' and weather_date >= (curdate()+ 1) order by curr_timestamp desc, weather_date asc limit 8) t1;"  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchone()
        temp = float("{0:.2f}".format(float(data[0])))
        print(temp)
        cursor.close()
        cnx.close()
        return temp

    def tomorrowWeatherDesc(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        #receiving description about tomorrow's weather
        query = "Select description, count(description) as num from (select * from future_data where city = 'Heidelberg' and weather_date >= (curdate()+ 1) order by curr_timestamp desc, weather_date asc limit 8) t1 group by description order by count(description) desc limit 1;"
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchone()
        temp = data[0]
        cursor.close()
        cnx.close()
        return temp

    def Nnext5DaysWeather(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        #receiving details about next 5 day's weather
        query = "SELECT avg(temperature - 273.15) as result from (select * from future_data where city = 'Heidelberg' order by curr_timestamp desc, weather_date asc limit 40) t1;"  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchone()
        temp = float("{0:.2f}".format(float(data[0])))
        cursor.close()
        cnx.close()
        return temp
    #chages to be done here to get all values from the database

    def Nnext5DaysWeatherdesc(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        query = "Select description, count(description) as num from (select * from future_data where city = 'Heidelberg' order by curr_timestamp desc, weather_date asc limit 40) t1;"
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchone()
        temp = data[0]
        cursor.close()
        cnx.close()
        return temp


    def next5DaysfullWeather(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        query = " SELECT weather_date,AVG(temperature - 273.15) AS result FROM (SELECT CAST(weather_date AS DATE) AS weather_date,temperature  FROM future_data WHERE city = 'Heidelberg' AND weather_date > CURDATE()+1 AND weather_date< CURDATE()+6 ) t1 GROUP BY weather_date;"  # actual SQL statement to be executed
        lines = cursor.execute(query)  # execute the query
        datax = cursor.fetchall() #only the last value is returning not all the values
        for row in datax:
            data = row
        temp = datax    
        #float("{0:.2f}".format(float(data[0])))
        cursor.close()
        cnx.close()
        return temp
    def last5DaysfullCurrent(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        query = "SELECT weather_date, SUM(current_output)FROM (SELECT CAST(curr_timestamp AS DATE) AS weather_date,current_output FROM current_data WHERE city = 'Heidelberg' AND curr_timestamp > CURDATE()-5 AND curr_timestamp< CURDATE()+1)) t1 GROUP BY weather_date;" #actual SQL statement to be executed- 18000 * config.powerFactor/ 1000000
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchall()
        #for row in data:
           # print(row)
        #temp = float("{0:.2f}".format(float(data1)))
        cursor.close()
        cnx.close()
        return data      

    def next5DaysfullCurrent(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        query = "SELECT weather_date, SUM(current_output) FROM (SELECT CAST(weather_date AS DATE) AS weather_date,current_output FROM future_data WHERE city = 'Heidelberg'AND weather_date > CURDATE()+1 AND weather_date< CURDATE()+6 ) t1 GROUP BY weather_date;" 
         #actual SQL statement to be executed- 18000 *3* config.powerFactor/ 1000000
        lines = cursor.execute(query)  # execute the query
        data = cursor.fetchall()
        #if data1 is None:
        #   data1 = 0.0
        #temp = float("{0:.2f}".format(float(data1)))

        cursor.close()
        cnx.close()
        return data

    def currentNow(self):
        # receiving present current 
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
        #print(url)
        f = requests.get(url,timeout=5)
        if(str(f)!="<Response [502]>" and str(f)!="<Response [500]>" and str(f)!="<Response [404]>"):
            ret = f
            jdata = f.json()
            powq = jdata[0] * config.powerFactor  # actual conversion
            ret = str(powq)
        else:
            ret=0    
        return float("{0:.2f}".format(float(ret)))

    def previousandnext5DaysfullCurrent(self):
        cnx = classCommonFunc.dataBaseConnection()
        cursor = cnx.cursor()
        query = "SELECT weather_date, SUM(current_output)*10800/1000000 FROM (SELECT CAST(weather_date AS DATE) AS weather_date,current_output FROM future_data WHERE city = 'Heidelberg'AND weather_date > CURDATE()+1 AND weather_date< CURDATE()+6 )t1 GROUP BY weather_date" 
        lines = cursor.execute(query)  
        data = cursor.fetchall()
        cursor.close()
        cnx.close()
        return data