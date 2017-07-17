import logging


from flask import Flask

from flask_ask import Ask, statement, question, session as ask_session

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def welcome():
    ask_session.attributes['date'] = None #'2017-07-16'
    ask_session.attributes['time'] = None #'03:00'
    ask_session.attributes['duration'] = None #'PT5M'

    return question('Hello, please tell me the dates and times when your meeting shall be scheduled')


@ask.intent("DateIntent")
def missing_duration_time(Date):
    ask_session.attributes['date'] = Date

    if ask_session.attributes['duration'] is None and ask_session.attributes['time'] is None:
        return question('What time is the meeting and how long is it?')
    elif ask_session.attributes['duration'] is not None and ask_session.attributes['time'] is None:
        missing_time(Date, ask_session.attributes['duration'])
    elif ask_session.attributes['time'] is not None and ask_session.attributes['duration'] is None:
        missing_duration(ask_session.attributes['date'], ask_session.attributes['time'])
    else:
        allKnown(ask_session.attributes['date'], ask_session.attributes['time'], ask_session.attributes['duration'])


@ask.intent("TimeIntent")
def missing_date_duration(Time):
    ask_session.attributes['time'] = Time
    if ask_session.attributes['date'] is None and ask_session.attributes['duration'] is None:
        return question('Whats the date and the duration of the meeting?')
    elif ask_session.attributes['date'] is not None and ask_session.attributes['duration'] is None:
        missing_duration(ask_session.attributes['date'], Time)
    elif ask_session.attributes['date'] is None and ask_session.attributes['duration'] is not None:
        missing_date(ask_session.attributes['time'], ask_session.attributes['duration'])
    else:
        allKnown(ask_session.attributes['date'], ask_session.attributes['time'], ask_session.attributes['duration'])


@ask.intent("DurationIntent")
def missing_date_time(Duration):
    ask_session.attributes['duration'] = Duration
    if ask_session.attributes['date'] is None and ask_session.attributes['time'] is None:
        return question('What day and what time is the meeting?')
    elif ask_session.attributes['date'] is not None and ask_session.attributes['time'] is None:
        missing_time(ask_session.attributes['date'], ask_session.attributes['duration'])
    elif ask_session.attributes['date'] is None and ask_session.attributes['time'] is not None:
        missing_date(ask_session.attributes['time'], ask_session.attributes['duration'])
    else:
        allKnown(ask_session.attributes['date'], ask_session.attributes['time'], ask_session.attributes['duration'])


@ask.intent("DateDurationIntent")
def missing_time(Date, Duration):
    ask_session.attributes['date'] = Date
    ask_session.attributes['duration'] = Duration
    if ask_session.attributes['time'] is None:
        return question('What time is the meeting?')
    else:
        allKnown(ask_session.attributes['date'], ask_session.attributes['time'], ask_session.attributes['duration'])



@ask.intent("DateTimeIntent")
def missing_duration(Date, Time):
    ask_session.attributes['date'] = Date
    ask_session.attributes['time'] = Time
    if ask_session.attributes['duration'] is None:
        return question('How long is the meeting?')
    else:
        allKnown(ask_session.attributes['date'], ask_session.attributes['time'], ask_session.attributes['duration'])



@ask.intent("TimeDurationIntent")
def missing_date(Time, Duration):
    ask_session.attributes['duration'] = Duration
    ask_session.attributes['time'] = Time
    if ask_session.attributes['date'] is None:
        return question('What day is the meeting?')
    else:
        allKnown(ask_session.attributes['date'], ask_session.attributes['time'], ask_session.attributes['duration'])



@ask.intent("DataTimeDurationIntent")
def allKnown(Date, Time, Duration):
    ask_session.attributes['date'] = Date
    ask_session.attributes['time'] = Time
    ask_session.attributes['duration'] = Duration
    return statement('The meeting is on ' + str(ask_session.attributes['date']) + ' at ' + str(ask_session.attributes['time']) + ' and lasts ' + str(ask_session.attributes['duration']))


if __name__ == '__main__':
    app.run(debug=True)


