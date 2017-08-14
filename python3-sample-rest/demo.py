from flask import Flask
from room_class import Room
from flask_ask import Ask, statement, question, session as ask_session

room = Room()

app = Flask(__name__)
ask = Ask(app, "/")

vars = {'date': None, 'time': None, 'duration': None, 'attendees': None}

# Amzazon Date: “today”: 2015-11-24
# Amazon Duration: “ten minutes”: PT10M, “five hours”: PT5H
# Amazon Time: “two fifteen pm”: 14:15
# MS DateTime: "2017-04-17T09:00:00",
# MS Duration : PT2H
def convert_amazon_to_ms(Date, Time):
    date_time = Date + 'T' + Time
    return date_time


@ask.launch
def welcome():
    ask_session.attributes['date'] = room.date = None  # '2017-07-16'
    ask_session.attributes['time'] = room.time = None  # '03:00'
    ask_session.attributes['duration'] = room.duration = None  # 'PT5M'
    return question('Hello, please tell me the dates and times when your meeting shall be scheduled')


@ask.intent("DateIntent")
def missing_duration_time(Date):
    room.date = ask_session.attributes['date'] = Date

    print('Date: ' + str(ask_session.attributes['date']))
    print('Date: ' + str(room.date))

    if room.duration is None and room.time is None:
        return question('What time is the meeting and how long is it?')
    elif room.duration is not None and room.time is None:
        return missing_time(room.date, room.duration)
    elif room.time is not None and room.duration is None:
        return missing_duration(room.date, room.time)
    else:
        print('DateIntent')
        return allKnown(Date, room.time, room.duration)


@ask.intent("TimeIntent")
def missing_date_duration(Time):
    room.time = ask_session.attributes['time'] = Time

    print('TimeIntent - Date: ' + str(room.date))
    print('TimeIntent - Time: ' + str(room.time))

    if room.date is None and room.duration is None:
        return question('Whats the date and the duration of the meeting?')
    elif room.date is not None and room.duration is None:
        return missing_duration(room.date, room.time)
    elif room.date is None and room.duration is not None:
        print('TimeIntent - duration!=null, date==null')
        return missing_date(room.time, room.duration)
    else:
        return allKnown(room.date, Time, room.duration)


@ask.intent("DurationIntent")
def missing_date_time(Duration):
    room.duration = ask_session.attributes['duration'] = Duration

    if room.date is None and room.time is None:
        return question('What day and what time is the meeting?')
    elif room.date is not None and room.time is None:
        return missing_time(room.date, room.duration)
    elif room.date is None and room.time is not None:
        return missing_date(room.time, room.duration)
    else:
        print('DurationIntent - All known   ')
        return allKnown(room.date, room.time, Duration)


@ask.intent("DateDurationIntent")
def missing_time(Date, Duration):
    room.date = ask_session.attributes['date'] = Date
    room.duration = ask_session.attributes['duration'] = Duration

    if room.time is None:
        return question('What time is the meeting?')
    else:
        return allKnown(Date, room.time, Duration)


@ask.intent("DateTimeIntent")
def missing_duration(Date, Time):
    room.date = ask_session.attributes['date'] = Date
    room.time = ask_session.attributes['time'] = Time
    print('DateTimeIntent Date: ' + str(room.date))
    print('DateTimeIntent Time: ' + str(room.time))

    if room.duration is None:
        print('DateTimeIntent no duration')
        # pprint(dir(question('How long is the meeting?')))
        return question('How long is the meeting?')
    else:
        return allKnown(Date, Time, room.duration)


@ask.intent("TimeDurationIntent")
def missing_date(Time, Duration):
    room.duration = ask_session.attributes['duration'] = Duration
    room.time = ask_session.attributes['time'] = Time
    ask_session.attributes['date'] = room.date

    if room.date is None:
        return question('What day is the meeting?')
    else:
        return allKnown(room.date, Time, Duration)


@ask.intent("DataTimeDurationIntent", convert={'Date': 'date', 'Time': 'time', 'Duration': 'timedelta'})
def allKnown(Date, Time, Duration):
    print('DataTimeDurationIntent ' + str(Date), str(Time), str(Duration))
    vars['date'] = Date
    vars['time'] = Time
    vars['duration'] = Duration
    return question("How many attendees will attend the meeting?")


@ask.intent("AttendeesIntent")
def numberOfAttendees(Attendees):
    vars['attendees'] = Attendees
    return statement('the meeting is on ' + room.date + ' at ' + room.time + ' and lasts ' + room.duration + ' . ' + Attendees + ' people are attending it. ')
    # return readMeetingTime(room.date, room.time, room.duration, Attendees)

# Print and return the meeting room
# def readMeetingTime(Date, Time, Duration, Attendees=0):
#     print('readMeetingTime')
#     get_infor_from_alexa(Date, Time, Duration,Attendees)
#     ask_session.attributes['date'] = ask_session.attributes['time'] = ask_session.attributes[
#         'duration'] = room.date = room.time = room.duration = None
#
#     start = '2017-07-19T10:00'
#     end = '2017-07-19T20:00'
#     # freeRoom = getFreeRooms(start, end)
#
#     # TODO get events from each calendar
#
#     # TODO convert duration in end time
#     #   convert start time in python time, (duration)
#     #   add time
#     # TODO loop through rooms (calendars)
#     # TODO get events at that time, time difference because if events in that time frame occur response is not null
#     # TODO create event, in one of the free rooms
#     # TODO frontend, fabric CSS and JS
#     # TODO name and number of attendees intents and parameters
#     return statement('The meeting is in room ' + str(freeRoom))
#     # return statement('The meeting is on ' + str(Date) + ' at ' + str(Time) + ' and lasts ' + str(Duration))


if __name__ == '__main__':
    app.run(debug=True)


