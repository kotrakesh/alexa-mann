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
    print(room.date, room.duration, room.time)
    return question('Hello, please tell me the dates and times when your meeting shall be scheduled')


@ask.intent("DateIntent")
def missing_duration_time(Date):
    room.date = Date
    if room.duration == '' and room.time == '':
        return question('What time is the meeting and how long is it?')
    elif room.duration != '' and room.time == '':
        missing_time(Date, room.duration)
    elif room.time != '' and room.duration == '':
        missing_duration(room.date, room.time)
    else:
        allKnown(room.date, room.time, room.duration)


@ask.intent("TimeIntent")
def missing_date_duration(Time):
    room.time = Time
    if room.date == '' and room.duration == '':
        return question('Whats the date and the duration of the meeting?')
    elif room.date != '' and room.duration == '':
        missing_duration(room.date, Time)
    elif room.date == '' and room.duration != '':
        missing_date(room.time, room.duration)
    else:
        return allKnown(room.date, room.time, room.duration)


@ask.intent("DurationIntent")
def missing_date_time(Duration):
    room.duration = Duration
    if room.date == '' and room.time == '':
        return question('What day and what time is the meeting?')
    elif room.date != '' and room.time == '':
        print('im here')
        missing_time(room.date, room.duration)
    elif room.date == '' and room.time != '':
        missing_date(room.timem, room.duration)
    else:
        return allKnown(room.date, room.time, room.duration)


@ask.intent("DateDurationIntent")
def missing_time(Date, Duration):
    print('number two')
    room.date = Date
    room.duration = Duration
    if room.time == '':
        print('three')
        return question('What time is the meeting?')
    else:
        return allKnown(room.date, room.time, room.duration)



@ask.intent("DateTimeIntent")
def missing_duration(Date, Time):
    room.date = Date
    room.time = Time
    if room.duration == '':
        return question('How long is the meeting?')
    else:
        return allKnown(room.date, room.time, room.duration)



@ask.intent("TimeDurationIntent")
def missing_date(Time, Duration):
    room.duration = Duration
    room.time = Time
    if room.date == '':
        return question('What day is the meeting?')
    else:
        return allKnown(room.date, room.time, room.duration)



@ask.intent("DataTimeDurationIntent")
def allKnown(Date, Time, Duration):
    room.date = Date
    room.time = Time
    room.duration = Duration
    return statement('The meeting is on ' + str(Date) + ' at ' + str(Time) + ' and lasts ' + str(Duration))



if __name__ == '__main__':
    app.run(debug=True)


