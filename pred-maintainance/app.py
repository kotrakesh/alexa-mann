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

def predective_maintenance():
	initial_help = render_template('initialhelp')
	return question(initial_help)

@ask.intent("YesterdayIntent")
def past_yesterday():
	currentRecieved = dbco.pastYesterday()
	pastCurrent = render_template('yesterdayCurrent', numbers=currentRecieved)
	return statement(pastCurrent)

@ask.intent("LastweekIntent")
def past_week():
	currentRecieved = dbco.pastlastWeek()
	pastWeekCurrent = render_template('lastweekCurrent', numbers=currentRecieved)
	return statement(pastWeekCurrent)

@ask.intent("TillnowcurrentIntent")
def present_tillNow():
	currentRecieved = dbco.tillNowCurrent()
	presentTillNowCurrent = render_template('todayCurrentTillNow', numbers=currentRecieved)
	return statement(presentTillNowCurrent)

@ask.intent("NowcurrentIntent")
def present_now():
	currentRecieved = dbco.currentNow()
	
	presentNowCurrent = render_template('todayCurrentNow', numbers=currentRecieved)
	return statement(presentNowCurrent)

@ask.intent("TodayaftercurrentIntent")
def present_after():
	currentRecieved = dbco.todayAfterCurrent()
	presentAfterCurrent = render_template('todayCurrentAfter', numbers=currentRecieved)
	return statement(presentAfterCurrent) 

@ask.intent("TodayweatherIntent")
def present_weather():
	weatherRecieved = dbco.todayWeather()
	presentWeather = render_template('todayWeather', numbers=weatherRecieved)
	return statement(presentWeather) 

#@ask.intent("NowweatherIntent")
#def present_Now_weather():
#	weatherRecieved = #------------------------------------------------
#	presentNowWeather = render_template('todayWeatherNow', numbers=weatherRecieved)
#	return statement(presentNowWeather) 

@ask.intent("TomorrowcurrentIntent")
def future_tomorrow_current():
	currentRecieved = dbco.tomorrowCurrent()
	futureTomorrowCurrent = render_template('tomorrowCurrent', numbers=currentRecieved)
	return statement(futureTomorrowCurrent) 

@ask.intent("NextweekcurrentIntent")
def future_week_current():
	currentRecieved = dbco.next5DaysCurrent()
	futureWeekCurrent = render_template('nextweekCurrent', numbers=currentRecieved)
	return statement(futureWeekCurrent)

@ask.intent("TomorroweatherIntent")
def future_Tomorrow_weather():
	weatherRecieved = dbco.tomorrowWeather()
	futureTomorrowWeather = render_template('tomorrowWeather', numbers=weatherRecieved)
	return statement(futureTomorrowWeather)  
@ask.intent("FailurePossibilityIntent")
def failure_weather():
	futureTomorrowWeather = render_template('failurePoss')
	return statement(futureTomorrowWeather)
@ask.intent("NextweekweatherIntent")
def future_Week_weather():
	weatherRecieved = dbco.Nnext5DaysWeather()
	futureWeekWeather = render_template('nextweekWeather', numbers=weatherRecieved)
	return statement(futureWeekWeather)	 
@app.route("/admin")
def admin():
    return ""

if __name__ == '__main__':

	app.run(debug=True)