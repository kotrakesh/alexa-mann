# Copyright (c) Microsoft. All rights reserved. Licensed under the MIT license.
# See LICENSE in the project root for license information.
"""Main program for Microsoft Graph API Connect demo."""
import json
import sys
import uuid
import logging
import datetime
from room_class import Room

# un-comment these lines to suppress the HTTP status messages sent to the console
# import logging
# logging.getLogger('werkzeug').setLevel(logging.ERROR)

import requests
from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauthlib.client import OAuth
from flask_ask import Ask, statement, question, session as ask_session
from pprint import pprint

room = Room()

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# read private credentials from text file
client_id, client_secret, *_ = open('_PRIVATE.txt').read().split('\n')
if (client_id.startswith('*') and client_id.endswith('*')) or \
        (client_secret.startswith('*') and client_secret.endswith('*')):
    print('MISSING CONFIGURATION: the _PRIVATE.txt file needs to be edited ' + \
          'to add client ID and secret.')
    sys.exit(1)

app = Flask(__name__)
app.debug = False
app.secret_key = 'development'
oauth = OAuth(app)
ask = Ask(app, "/")

vars = {'date': None, 'time': None, 'duration': None, 'attendees': None}

# since this sample runs locally without HTTPS, disable InsecureRequestWarning
requests.packages.urllib3.disable_warnings()

# scopes =

msgraphapi = oauth.remote_app( \
    'microsoft',
    consumer_key=client_id,
    consumer_secret=client_secret,
    #    request_token_params={'scope': 'User.Read Mail.Send'},
    request_token_params={'scope': 'User.Read Mail.Send Calendars.ReadWrite'},
    base_url='https://graph.microsoft.com/v1.0/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
    authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
)


@app.route('/')
def index():
    """Handler for home page."""
    return login()
    return render_template('connect.html')


# https://forums.developer.amazon.com/questions/5428/how-to-link-an-amazon-alexa-skill-using-azure-app.html
# http://www.macadamian.com/2016/03/24/creating-a-new-alexa-skill/

@app.route('/login')
def login():
    """Handler for login route."""
    guid = uuid.uuid4()  # guid used to only accept initiated logins
    session['state'] = guid
    return msgraphapi.authorize(callback=url_for('authorized', _external=True), state=guid)


@app.route('/logout')
def logout():
    """Handler for logout route."""
    session.pop('microsoft_token', None)
    session.pop('state', None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    """Handler for login/authorized route."""
    response = msgraphapi.authorized_response()

    if response is None:
        return "Access Denied: Reason={0}\nError={1}".format( \
            request.args['error'], request.args['error_description'])

    # Check response for state
    if str(session['state']) != str(request.args['state']):
        raise Exception('State has been messed with, end authentication')
    session['state'] = ''  # reset session state to prevent re-use

    # Okay to store this in a local variable, encrypt if it's going to client
    # machine or database. Treat as a password.
    session['microsoft_token'] = (response['access_token'], '')
    # Store the token in another session variable for easy access
    session['access_token'] = response['access_token']
    me_response = msgraphapi.get('me')
    me_data = json.loads(json.dumps(me_response.data))
    username = me_data['displayName']
    email_address = me_data['userPrincipalName']
    session['alias'] = username
    session['userEmailAddress'] = email_address
    room.token = session['access_token']
    return redirect('main')


@app.route('/main')
def main():
    get_calendars()  # directly load the calenders after login
    """Handler for main route."""
    if session['alias']:
        username = session['alias']
        email_address = session['userEmailAddress']
        return render_template('main.html', name=username, emailAddress=email_address)
    else:
        return render_template('main.html')


# Get Information about the current account
@app.route('/me')
def get_me():
    me_response = msgraphapi.get('me')
    me_data = json.loads(json.dumps(me_response.data))
    username = me_data['displayName']
    vname = me_data['givenName']
    nname = me_data['surname']
    userid = me_data['id']
    email_address = me_data['userPrincipalName']

    return render_template('me.html', vName=vname, nName=nname, uID=userid, mail=email_address)


@app.route('/calendars')
def get_calendars():
    cal = msgraphapi.get('me/calendars')
    cal_data = json.loads(json.dumps(cal.data))
    room.data = cal_data
    response = call_getcalendar_endpoint(session['access_token'])
    if response == 'SUCCESS':
        show_success = 'true'
        show_error = 'false'
    else:
        print(response)
        show_success = 'false'
        show_error = 'true'

    return render_template('calendars.html', name=session['alias'], data=cal, jsondata=cal_data, showCalendars=1,
                           aDate=vars['date'], aTime=vars['time'], aDuration=vars['duration'])


@app.route('/create_calendar')
def create_calendar():
    """Handler for send_mail route."""
    username = request.args.get('name')  # get name of the user the calendar is created for

    response = call_createcalendar_endpoint(session['access_token'], username)

    if response == 'SUCCESS':
        show_success = 'true'
        show_error = 'false'
    else:
        print(response)
        show_success = 'false'
        show_error = 'true'

    session['pageRefresh'] = 'false'
    return render_template('main.html', name=session['alias'], username=username,
                           showSuccess_createCalendar=show_success, showError_createCalendar=show_error)


@app.route('/send_mail')
def send_mail():
    """Handler for send_mail route."""
    email_address = request.args.get('emailAddress')  # get email address from the form
    response = call_sendmail_endpoint(session['access_token'], session['alias'], email_address)
    if response == 'SUCCESS':
        show_success = 'true'
        show_error = 'false'
    else:
        print(response)
        show_success = 'false'
        show_error = 'true'

    session['pageRefresh'] = 'false'
    return render_template('main.html', name=session['alias'],
                           emailAddress=email_address, showSuccess=show_success,
                           showError=show_error)


@app.route('/list_events')
def list_events():
    cal_id = request.args.get('cal_id')  # get email address from the form
    cal_name = request.args.get('cal_name')
    response = call_listevents_endpoint(session['access_token'], cal_id)
    data = json.loads(response.text)
    print(data)
    if response.ok:
        show_success = 'true'
        show_error = 'false'
    else:
        print(response)
        show_success = 'false'
        show_error = 'true'

    session['pageRefresh'] = 'false'
    print(response)

    return render_template('calendars.html', name=session['alias'], calName=cal_name, data=data,
                           showSuccess_listEvents=show_success, showError_listEvents=show_error, showEvents=1)


@app.route('/list_events_for_time')
def list_events_for_time():
    cal_id = request.args.get('cal_id')  # get email address from the form
    cal_name = request.args.get('cal_name')
    cal_date = request.args.get('date')
    cal_start_time = request.args.get('start_time')
    cal_end_time = request.args.get('end_time')
    start = convert_amazon_to_ms(cal_date, cal_start_time)
    end = convert_amazon_to_ms(cal_date, cal_end_time)
    response = call_listevents_for_time_endpoint(session['access_token'], cal_id, start, end)
    data = json.loads(response.text)

    print(cal_name, cal_date, cal_start_time, cal_end_time)
    if response.ok:
        show_success = 'true'
        show_error = 'false'
    else:
        print(response)
        show_success = 'false'
        show_error = 'true'

    session['pageRefresh'] = 'false'
    print(response)

    return render_template('calendars.html', name=session['alias'], calName=cal_name, data=data,
                           showSuccess_listEvents=show_success, showError_listEvents=show_error, showEvents=1)


@app.route('/create_event')
def create_event(start, end, title, roomName):
    """Handler for create_event route."""
    response = call_createvent_endpoint(session['access_token'], start, end, title, roomName)
    if response == 'SUCCESS':
        show_success = 'true'
        show_error = 'false'
    else:
        print(response)
        show_success = 'false'
        show_error = 'true'

    session['pageRefresh'] = 'false'
    return render_template('main.html', name=session['alias'], data=response, showSuccess=show_success,
                           showError=show_error)


@app.route('/get_information')
def get_information():
    return render_template('information.html', aDate=vars['date'], aTime=vars['time'], aDuration=vars['duration'], aAttendees=vars['attendees'])


##################################


# If library is having trouble with refresh, uncomment below and implement
# refresh handler see https://github.com/lepture/flask-oauthlib/issues/160 for
# instructions on how to do this. Implements refresh token logic.
# @app.route('/refresh', methods=['POST'])
# def refresh():
@msgraphapi.tokengetter
def get_token():
    """Return the Oauth token."""
    return session.get('microsoft_token')


def call_listevents_endpoint(access_token, id):
    list_events_url = 'https://graph.microsoft.com/v1.0/me/calendars/' + id + '/events'
    # set request headers
    headers = {'User-Agent': 'python_tutorial/1.0',
               'Authorization': 'Bearer {0}'.format(access_token),
               'Accept': 'application/json',
               'Content-Type': 'application/json'}

    request_id = str(uuid.uuid4())
    instrumentation = {'client-request-id': request_id,
                       'return-client-request-id': 'true'}
    headers.update(instrumentation)

    response = requests.get(url=list_events_url,
                            headers=headers,
                            verify=False,
                            params=None)

    if response.ok:
        return response
    else:
        return '{0}: {1}'.format(response.status_code, response.text)


def call_listevents_for_time_endpoint(access_token, id, start, end):
    list_events_url = 'https://graph.microsoft.com/v1.0/me/calendars/' + id + '/calendarView?startDateTime=' + start + 'Z&endDateTime=' + end + 'Z'
    # set request headers
    print(start, end)
    headers = {'User-Agent': 'python_tutorial/1.0',
               'Authorization': 'Bearer {0}'.format(access_token),
               'Accept': 'application/json',
               'Content-Type': 'application/json'}

    request_id = str(uuid.uuid4())
    instrumentation = {'client-request-id': request_id,
                       'return-client-request-id': 'true'}
    headers.update(instrumentation)

    response = requests.get(url=list_events_url,
                            headers=headers,
                            verify=False,
                            params=None)
    print("test100")
    if response.ok:
        return response
    else:
        return '{0}: {1}'.format(response.status_code, response.text)


def call_createcalendar_endpoint(access_token, name):
    create_calendar_url = 'https://graph.microsoft.com/v1.0/me/calendars'
    # set request headers
    headers = {'User-Agent': 'python_tutorial/1.0',
               'Authorization': 'Bearer {0}'.format(access_token),
               'Accept': 'application/json',
               'Content-Type': 'application/json'}

    request_id = str(uuid.uuid4())
    instrumentation = {'client-request-id': request_id,
                       'return-client-request-id': 'true'}
    headers.update(instrumentation)
    user_data = {'name': name}

    response = requests.post(url=create_calendar_url,
                             headers=headers,
                             data=json.dumps(user_data),
                             verify=False,
                             params=None)

    if response.ok:
        return 'SUCCESS'
    else:
        return '{0}: {1}'.format(response.status_code, response.text)


def call_sendmail_endpoint(access_token, name, email_address):
    """Call the resource URL for the sendMail action."""
    send_mail_url = 'https://graph.microsoft.com/v1.0/me/microsoft.graph.sendMail'

    # set request headers
    headers = {'User-Agent': 'python_tutorial/1.0',
               'Authorization': 'Bearer {0}'.format(access_token),
               'Accept': 'application/json',
               'Content-Type': 'application/json'}

    # Use these headers to instrument calls. Makes it easier to correlate
    # requests and responses in case of problems and is a recommended best
    # practice.
    request_id = str(uuid.uuid4())
    instrumentation = {'client-request-id': request_id,
                       'return-client-request-id': 'true'}
    headers.update(instrumentation)

    # Create the email that is to be sent via the Graph API
    email = {'Message': {'Subject': 'Welcome to the Microsoft Graph Connect sample for Python',
                         'Body': {'ContentType': 'HTML',
                                  'Content': render_template('email.html', name=name)},
                         'ToRecipients': [{'EmailAddress': {'Address': email_address}}]
                         },
             'SaveToSentItems': 'true'}

    response = requests.post(url=send_mail_url,
                             headers=headers,
                             data=json.dumps(email),
                             verify=False,
                             params=None)

    if response.ok:
        return 'SUCCESS'
    else:
        return '{0}: {1}'.format(response.status_code, response.text)


def call_createvent_endpoint(access_token,tStart,tEnd,title,roomName):
    """Call the resource URL for the create event action."""
    send_event_url = 'https://graph.microsoft.com/v1.0/me/events'
    print("test2")
    # set request headers
    headers = {'User-Agent': 'python_tutorial/1.0',
               'Authorization': 'Bearer {0}'.format(access_token),
               'Accept': 'application/json',
               'Content-Type': 'application/json'
               }

    # Use these headers to instrument calls. Makes it easier to correlate
    # requests and responses in case of problems and is a recommended best
    # practice.
    request_id = str(uuid.uuid4())
    instrumentation = {'client-request-id': request_id,
                       'return-client-request-id': 'true'}
    headers.update(instrumentation)

    # Create the email that is to be sent via the Graph API
    event = {
        "subject": title,
        "body": {
            "contentType": "HTML",
            "content": "Does late morning work for you?"
        },
        "start": {
            "dateTime": tStart,
            "timeZone": "Pacific Standard Time"
        },
        "end": {
            "dateTime": tEnd,
            "timeZone": "Pacific Standard Time"
        },
        "location": {
            "displayName": roomName
        },
        #"attendees": [
        #   {
        #        "emailAddress": {
        #            "address": "fannyd@contoso.onmicrosoft.com",
        #           "name": "Fanny Downs"
        #        },
        #        "type": "required"
        #   }
        #]
    }

    response = requests.post(url=send_event_url,
                             headers=headers,
                             data=json.dumps(event),
                             verify=False,
                             params=None)

    if response.ok:
        return 'SUCCESS'
    else:
        return '{0}: {1}'.format(response.status_code, response.text)


def call_getcalendar_endpoint(access_token):
    """Call the resource URL for the sendMail action."""
    send_calendar_url = 'https://graph.microsoft.com/v1.0/me/microsoft.graph.calendars'

    # set request headers
    headers = {'User-Agent': 'python_tutorial/1.0',
               'Authorization': 'Bearer {0}'.format(access_token),
               'Accept': 'application/json',
               'Content-Type': 'application/json'}

    # Use these headers to instrument calls. Makes it easier to correlate
    # requests and responses in case of problems and is a recommended best
    # practice.
    request_id = str(uuid.uuid4())
    instrumentation = {'client-request-id': request_id,
                       'return-client-request-id': 'true'}
    headers.update(instrumentation)

    # Create the email that is to be sent via the Graph API
    response = requests.get(url=send_calendar_url, headers=headers)

    if response.ok:
        return 'SUCCESS'
    else:
        return '{0}: {1}'.format(response.status_code, response.text)


################################################################################################################3





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
    return readMeetingTime(room.date, room.time, room.duration, Attendees)


def getFreeRooms(t_start, t_end):
    print('getFreeRooms')

    # TODO authenticate with Graph API
    print('--------------------- login token: ' + str(room.token))
    # cal = call_getcalendar_endpoint(room.token)
    print(str(t_start), str(t_end), ' --- cal.data: ')

    # cal_data = json.loads(json.dumps(cal))
    print(room.data['value'])

    for cal in room.data['value']:
        print(' ------------ ')
        print('id: ' + str(cal['id']))
        print('name: ' + str(cal['name']))
        if (cal['name'] == 'Birthdays'):
            continue
        jdata = call_listevents_for_time_endpoint(room.token, cal['id'], t_start, t_end)
        data = json.loads(jdata.text)
        print(data['value'])
        if not data['value']:
            print('Keine Events vorhanden')
            print(data['value'])
            # TODO create Event for that date
            #create_event(t_start, t_end, "Event title", "Romm name")
            # TODO check other constraints like room size
            return cal['name']

        else:
            print('Events vorhanden')
            print(data['value'])
            # TODO continue to search


# Print and return the meeting room
def readMeetingTime(Date, Time, Duration, Attendees=0):
    print('readMeetingTime')
    get_infor_from_alexa(Date, Time, Duration,Attendees)
    ask_session.attributes['date'] = ask_session.attributes['time'] = ask_session.attributes[
        'duration'] = room.date = room.time = room.duration = None

    start = '2017-07-19T10:00'
    end = '2017-07-19T20:00'
    freeRoom = getFreeRooms(start, end)

    # TODO get events from each calendar

    # TODO convert duration in end time
    #   convert start time in python time, (duration)
    #   add time
    # TODO loop through rooms (calendars)
    # TODO get events at that time, time difference because if events in that time frame occur response is not null
    # TODO create event, in one of the free rooms
    # TODO frontend, fabric CSS and JS
    # TODO name and number of attendees intents and parameters
    return statement('The meeting is in room ' + str(freeRoom))
    # return statement('The meeting is on ' + str(Date) + ' at ' + str(Time) + ' and lasts ' + str(Duration))


def get_infor_from_alexa(Date, Time, Duration, Attendees):
    print(Date, Time, Duration,Attendees)
    vars['date'] = Date
    vars['time'] = Time
    vars['duration'] = Duration
    vars['attendees'] = Attendees
