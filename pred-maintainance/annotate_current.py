import datetime
import time
import random



def estimate_current(desc, occtime, temp, sunrise, sunset):
    retValue = 0.0 #not used
    tempC = temp - 273.15 #not used

    # calculate the sunrise hours and the current time in the format of a string: HH:MM:SS in order to compare later
    t1 = datetime.datetime.strptime(occtime, '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
    #sunriseTime - 2 hours
    sunriseHourm2 = time.strftime('%H:%M:%S', time.gmtime(sunrise + 7200 - 7200))
    #sunsetTime + 2 hours
    sunsetHourp2 = time.strftime('%H:%M:%S', time.gmtime(sunset + 7200 + 7200))
    sunriseHour = time.strftime('%H:%M:%S', time.gmtime(sunrise + 7200))
    sunsetHour = time.strftime('%H:%M:%S', time.gmtime(sunset + 7200))

    # scale from 0 to 640
    if (t1 < sunriseHourm2 or t1 > sunsetHourp2): #time at night when no current will be transmitted
        retValue = 0.0
    elif (t1 < sunriseHour or t1 > sunsetHour): #early morning low values / late evening low values
        if (desc == "clear sky"): #take a look whether there is clear sky or clouds etc.
            retValue = random.uniform(50.0, 150.0)
        else:
            retValue = random.uniform(50.0, 150.0) * 0.6 #make the value lower if there is no clear sky
    elif (t1 < '07:00:00' or t1 > '19:00:00'): #if earlier than 7 am or later than 7 pm
        if (desc == "clear sky"):
            retValue = random.uniform(150.0, 300.0)
        else:
            retValue = random.uniform(150.0, 300.0) * 0.6
    elif (t1 < '08:00:00' or t1 > '18:30:00'):
        if (desc == "clear sky"):
            retValue = random.uniform(250.0, 450.0)
        else:
            retValue = random.uniform(250.0, 450.0) * 0.6
    elif (t1 < '10:00:00' or t1 > '16:00:00'):
        if (desc == "clear sky"):
            retValue = random.uniform(350.0, 550.0)
        else:
            retValue = random.uniform(350.0, 550.0) * 0.7
    else:
        if (desc == "clear sky"): #time inbetween 10am and 4pm -> highest values
            retValue = random.uniform(500.0, 640.0)
        else:
            retValue = random.uniform(450.0, 640.0) * 0.75

    return ("%.2f" % retValue) # format the output as float like 0.00


def reevall():
    db = MySQLdb.connect(host="eu-cdbr-west-01.cleardb.com",
                         user="b3465148a734be",
                         passwd="a2c4eda1",
                         db="heroku_c0277ef6294fdf7")
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM current_data where current_output is null")
    rows = cur.fetchall()
    i = 0
    for row in rows:
        cur2 = db.cursor()
        sql1 = "update current_data set current_output = " + estimate_current(row['description'],
                                                                              row['curr_timestamp'].strftime(
                                                                                  '%Y-%m-%d %H:%M:%S'),
                                                                              row['temperature'], row['sunrise'],
                                                                              row['sunset']) + ' where id = ' + str(row['id']) + ';'
        i = i + 1
        print(i)
        try:
            cur2.execute(sql1)
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
    cur2.execute('commit;')

#reevall()
