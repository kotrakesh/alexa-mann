import logging


from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

from Test import Room

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

#date = ''
#time = ''
#duration = ''
room = Room()

@ask.launch
def welcome():
    return question('Hello, please tell me the dates and times when your meeting shall be scheduled')


@ask.intent("DateIntent")
def missing_duration_time():

    room.date = 2

    if (room.duration == '' and room.time == ''):
        return question('What time is the meeting and how long is it?')
    elif (room.duration != '' and room.time == ''):
        missing_time()
    elif (room.time != '' and room.duration == ''):
        missing_duration()
    else:
        allKnown()


@ask.intent("TimeIntent")
def missing_date_duration():
    room.time = 2
    if (room.date == '' and room.duration == ''):
        return question('Whats the date and the duration of the meeting?')
    elif (room.date != '' and room.duration == ''):
        missing_duration()
    elif (room.date == '' and room.duration != ''):
        missing_date()
    else:
        return allKnown()


@ask.intent("DurationIntent")
def missing_date_time():
    room.duration = 2
    if (room.date == '' and room.time == ''):
        return question('What day and what time is the meeting?')
    elif (room.date != '' and room.time == ''):
        missing_time()
    elif (room.date == '' and room.time != ''):
        missing_date()
    else:
        return allKnown()


@ask.intent("DateDurationIntent")
def missing_time():
    room.date = 2
    room.duration = 2
    if (room.time == ''):
        return question('What time is the meeting?')
    else:
        return allKnown()



@ask.intent("DateTimeIntent")
def missing_duration():
    date = 2
    time = 2
    if (room.duration == ''):
        return question('How long is the meeting?')
    else:
        return allKnown()



@ask.intent("TimeDurationIntent")
def missing_date():
    room.duration = 2
    room.time = 2
    if (room.date == ''):
        return question('What day is the meeting?')
    else:
        return allKnown()



@ask.intent("DataTimeDurationIntent")
def allKnown():
    return statement('blablabla', room.date, room.duration, room.time)






