# Copyright (c) Microsoft. All rights reserved. Licensed under the MIT license.
# See LICENSE in the project root for license information.
"""Main program for Microsoft Graph API Connect demo."""
import json
import sys
import uuid
import logging
import requests

from flask     import Flask, redirect, url_for, session, request, render_template
from flask_ask import Ask, statement, question, session as ask_session
from flask_oauthlib.client import OAuth

#Custom
from durationparser import getMeetingEndTime
from room_class import Room
from ms_graph_endpoint import call_createvent_endpoint, call_listevents_for_time_endpoint, call_createcalendar_endpoint, call_deletecalendar_endpoint
from utilities import convert_amazon_to_ms, get_infor_from_alexa, create_room_to_json

from package_msgraph import app

room = Room()

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# read private credentials from text file
client_id, client_secret, *_ = open('_PRIVATE.txt').read().split('\n')
if (client_id.startswith('*') and client_id.endswith('*')) or \
        (client_secret.startswith('*') and client_secret.endswith('*')):
    print('MISSING CONFIGURATION: the _PRIVATE.txt file needs to be edited ' + \
          'to add client ID and secret.')
    sys.exit(1)

#app = Flask('__main__')
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)
ask = Ask(app, "/")

vars = {'date': None, 'time': None, 'duration': None, 'attendees': None}

# since this sample runs locally without HTTPS, disable InsecureRequestWarning
requests.packages.urllib3.disable_warnings()


### Intents


@ask.launch
def welcome():
    print('welcome')
    room.date = None  # '2017-07-16'
    room.time = None  # '03:00'
    room.duration = None  # 'PT5M'
    return question(render_template('msg_launch_request'))


@ask.intent("DateIntent")
def missing_duration_time(Date):
    room.date = Date

    print('Date: ' + str(ask_session.attributes['date']))
    print('Date: ' + str(room.date))

    if (room.duration is None or not room.duration) and (room.time is None or not room.time):
        return question(render_template('msg_missing_duration_time'))
    elif room.duration and not room.time:
        return missing_time(room.date, room.duration)
    elif room.time and not room.duration:
        return missing_duration(room.date, room.time)
    else:
        print('DateIntent')
        return allKnown(Date, room.time, room.duration)


@ask.intent("TimeIntent")
def missing_date_duration(Time):
    room.time = Time
    print('TimeIntent - Date: ' + str(room.date))
    print('TimeIntent - Time: ' + str(room.time))
    if Time == '':
        print('############################\n Time is empty')
        room.time = None

    if not room.date and not room.duration:
        return question(render_template('msg_missing_date_duration'))
    elif room.date and not room.duration:
        return missing_duration(room.date, room.time)
    elif not room.date and room.duration:
        print('TimeIntent - duration!=null, date==null')
        return missing_date(room.time, room.duration)
    else:
        return allKnown(room.date, Time, room.duration)


@ask.intent("DurationIntent")
def missing_date_time(Duration):
    print('durations')
    room.duration = ask_session.attributes['duration'] = Duration

    if not room.date and not room.time:
        return question(render_template('msg_missing_date_time'))
    elif room.date and not room.time:
        return missing_time(room.date, room.duration)
    elif not room.date and room.time:
        return missing_date(room.time, room.duration)
    else:
        print('DurationIntent - All known   ')
        return allKnown(room.date, room.time, Duration)


@ask.intent("DateDurationIntent")
def missing_time(Date, Duration):
    room.date = Date
    room.duration = Duration

    if not room.time:
        return question(render_template('msg_missing_time'))
    else:
        return allKnown(room.date, room.time, room.duration)


@ask.intent("DateTimeIntent")
def missing_duration(Date, Time):
    room.date = Date
    room.time = Time

    if not room.duration:
        print('DateTimeIntent no duration')
        return question(render_template('msg_missing_duration'))
    else:
        return allKnown(room.date, room.time, room.duration)


@ask.intent("TimeDurationIntent")
def missing_date(Time, Duration):
    room.duration = Duration
    room.time = Time
    if not room.date:
        return question(render_template('msg_missing_date'))
    else:
        return allKnown(room.date, room.time, room.duration)


@ask.intent("DataTimeDurationIntent")
def allKnown(Date, Time, Duration):
    room.date = Date
    room.time = Time
    room.duration = Duration
    print('DataTimeDurationIntent ' + str(Date), str(Time), str(Duration))
    vars['date'] = Date
    vars['time'] = Time
    vars['duration'] = Duration
    return question(render_template('msg_attendees'))


@ask.intent("AttendeesIntent")
def numberOfAttendees(Attendees):
    room.attendees = vars['attendees'] = Attendees
    if not room.duration or not room.date or not room.time:
        return question("Please, specify the date, time and the duration first")
    #TODO specify missing information
    return question(render_template('msg_title'))


@ask.intent("TitleIntent")
def title_of_event(Title):
    if room.date and not room.time and room.duration:
        return missing_time(room.date, room.duration)
    if not room.date and room.time and room.duration:
        return missing_date(room.time, room.duration)
    if room.date and room.time and not room.duration:
        return missing_duration(room.date, room.time)
    else:
        return readMeetingTime(room.date, room.time, room.duration, room.attendees, Title)



### Alexa Utilities

# Print and return the meeting room
def readMeetingTime(Date, Time, Duration, Attendees, Title):
    print('readMeetingTime')
    get_infor_from_alexa(Date, Time, Duration,Attendees)
    ask_session.attributes['date'] = ask_session.attributes['time'] = ask_session.attributes['duration'] = room.date = room.time = room.duration = None

    start = convert_amazon_to_ms(Date, Time)
    am_end = getMeetingEndTime(Time, Duration)
    end = convert_amazon_to_ms(Date, am_end)


    result = getFreeRooms(start, end, Attendees, Title)

    if (result['roomFound'] == 1):
        return statement(render_template('msg_booked_room_success', roomname=result['roomName']))\
            .simple_card(title=render_template('card_booked_room_success_title'), content= render_template('card_booked_room_success_content', roomname=result['roomName'], start=start, end=end, attendees=Attendees))
    else:
        return statement(render_template('msg_booked_room_fail', fail_reason=result['reason']))\
            .simple_card(title=render_template('card_booked_room_fail_title'), content=render_template('card_booked_room_fail_content', fail_reason=result['reason']))

def getFreeRooms(t_start, t_end, attendees, title):

    # TODO authenticate with Graph API

    print(str(t_start), str(t_end), ' Attendees: ', str(attendees), ' ', str(title), ' --- cal.data: ')


    locConstraint = json.load(open('locationConstraint.json'))
    if(room.data is None):
        return {'roomFound': 0, 'roomName': '', 'reason': 'Error while loading rooms'}

    for cal in room.data['value']:
        if (cal['name'] == 'Calendar' or cal['name'] == 'Birthdays' or cal['name'] == 'Room 3'): # calendar and    birthdays are ignored
            continue

        print(' ------------ ')
        print('name: ' + str(cal['name']))

        jdata = call_listevents_for_time_endpoint(room.token, cal['id'], t_start, t_end)

#        if (jdata['401'] is not None):
#            return {'roomFound': False, 'roomName': cal['name'], 'reason': 'Error while connecting to MS Graph API'}

        data = json.loads(jdata.text)

        #print(data['value'])

        if not data['value']:
            print('Keine Events vorhanden')

            for l in locConstraint['locations']:

                if l['displayName'] == cal['name']:
                    if int(attendees) <= int(l['maxAttendees']):
                        print('Raumgroesse: ' +  str(attendees), ' max: ', str(l['maxAttendees']))
                        print('Das Meeting findet in Raum ' + cal['name'] + ' statt!')
                        print('    ')

                        create_event_from_alexa(t_start, t_end, title, cal['name'], cal['id'])

                        return {'roomFound': 1, 'roomName': cal['name'], 'reason': 'All rooms are booked'}
                    else:
                        print('Raumgroesse: ' + str(attendees), ' > ', str(l['maxAttendees']))
                        print('Raum ist zu klein')

        else:
            print('Events vorhanden')
    return {'roomFound': 0, 'roomName': cal['name'], 'reason': 'No free room was found'}

def create_event_from_alexa(start, end, title, room_name, cal_id):
    """Handler for create_event route."""
    print("cal id:"+cal_id)
    call_createvent_endpoint(room.token, start, end, title, room_name, cal_id)




