import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from dataBaseAccess_main import dbc

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)
dbco = dbc()


@ask.launch
def predective_maintenance(): #Basic help
    initial_help = render_template('initialhelp')
    return question(initial_help)

@ask.intent("AMAZON.HelpIntent")
def intent_help():
    return question(render_template('msghelp'))

@ask.intent("AMAZON.CancelIntent")
def intent_cancel():
    return statement(render_template('msgbye'))

@ask.intent("AMAZON.StopIntent")
def intent_stop():
    return statement(render_template('msgbye'))

@ask.intent("YesterdayIntent")
def past_yesterday():# To retrieve yesterday current
    currentRecieved = dbco.pastYesterday()
    pastCurrent = render_template('yesterdayCurrent', numbers=currentRecieved)
    return question(pastCurrent)


@ask.intent("LastweekIntent")
def past_week():#To retrieve last week current
    currentRecieved = dbco.pastlastWeek()
    pastWeekCurrent = render_template('lastweekCurrent', numbers=currentRecieved)
    return question(pastWeekCurrent)


@ask.intent("TillnowcurrentIntent")
def present_tillNow():#To retrieve current till the current time
    currentRecieved = dbco.tillNowCurrent()
    presentTillNowCurrent = render_template('todayCurrentTillNow', numbers=currentRecieved)
    return question(presentTillNowCurrent)


@ask.intent("NowcurrentIntent")
def present_now():#To retrieve current at present time
    currentRecieved = dbco.currentNow()
    presentNowCurrent = render_template('todayCurrentNow', numbers=currentRecieved)
    return question(presentNowCurrent)


@ask.intent("TodayaftercurrentIntent")
def present_after():# To retrieve current expected for today
    currentRecieved = dbco.todayAfterCurrent()
    presentAfterCurrent = render_template('todayCurrentAfter', numbers=currentRecieved)
    return question(presentAfterCurrent)


@ask.intent("TodayweatherIntent")
def present_weather():#To retrieve today's weather data
    weatherRecieved = dbco.todayWeather()
    descRecieved = dbco.todayWeatherDesc()
    presentWeather = render_template('todayWeather', numbers=weatherRecieved, desc=descRecieved)
    return question(presentWeather)

@ask.intent("NowweatherIntent")
def present_Now_weather():#To retrieve present weather data
    weatherRecieved = dbco.nowWeather()
    presentNowWeather = render_template('todayWeatherNow', numbers=weatherRecieved[0], desc=weatherRecieved[1], city=weatherRecieved[2])
    return question(presentNowWeather)

@ask.intent("TomorrowcurrentIntent")
def future_tomorrow_current():#To retrieve tomorrow expected current
    currentRecieved = dbco.tomorrowCurrent()
    futureTomorrowCurrent = render_template('tomorrowCurrent', numbers=currentRecieved)
    return question(futureTomorrowCurrent)


@ask.intent("NextweekcurrentIntent")
def future_week_current():#To retrieve current expected for net 5 day's
    currentRecieved = dbco.next5DaysCurrent()
    futureWeekCurrent = render_template('nextweekCurrent', numbers=currentRecieved)
    return question(futureWeekCurrent)


@ask.intent("TomorroweatherIntent")
def future_Tomorrow_weather():#To retrieve tomorrow weather data
    weatherRecieved = dbco.tomorrowWeather()
    descRecieved = dbco.tomorrowWeatherDesc()
    futureTomorrowWeather = render_template('tomorrowWeather', numbers=weatherRecieved, desc=descRecieved)
    return question(futureTomorrowWeather)


@ask.intent("FailurePossibilityIntent")
def failure_weather():
    futureTomorrowWeather = render_template('failurePoss')
    return question(futureTomorrowWeather)


@ask.intent("FalseFailurePossibilityIntent")
def failure_weather():
     return question(render_template('failurePoss2'))


@ask.intent("NextweekweatherIntent")
def future_Week_weather():#To retrieve next week weather data
    weatherRecieved = dbco.Nnext5DaysWeather()
    descRecieved = dbco.Nnext5DaysWeatherdesc()
    futureWeekWeather = render_template('nextweekWeather', numbers=weatherRecieved, desc=descRecieved)
    return question(futureWeekWeather)

@app.route("/nextweekweather")
def next_Week_weather():
    weatherRecieved = dbco.next5DaysfullWeather()
    return repr(weatherRecieved)

@app.route("/nextweekCurrent")
def next_Week_current():
    currentRecieved = dbco.next5DaysfullCurrent()
    return repr(currentRecieved)

@app.route("/tomorroweather")
def tomorrow_weather():
    weatherRecieved = dbco.tomorrowWeather()
    return repr(weatherRecieved)

@app.route("/tomorrowCurrent")
def tomorrow_Current():
    currentRecieved = dbco.tomorrowCurrent()
    return repr(currentRecieved)


@app.route("/")
def admin():# method to route with localhost
    pastYesterday =  dbco.pastYesterday()
    currentNow = dbco.currentNow()
    tomorrowCurrent = dbco.tomorrowCurrent()
    return render_template('%s.html' % 'index',pastYesterday=pastYesterday,currentNow =currentNow, tomorrowCurrent = tomorrowCurrent)#
    
if __name__ == '__main__':
    app.run(debug=True) 