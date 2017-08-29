
import json
import sys
import uuid
import logging
import requests

from flask     import Flask, redirect, url_for, session, request, render_template
#from flask_ask import Ask, statement, question, session as ask_session
from flask_oauthlib.client import OAuth

#Custom

#from durationparser import getMeetingEndTime
from room_class import Room
#from alexa_custom_skill import *
from ms_graph_endpoint import call_createvent_endpoint, call_listevents_for_time_endpoint, call_createcalendar_endpoint, call_deletecalendar_endpoint
from utilities import convert_amazon_to_ms, get_infor_from_alexa, create_room_to_json
#import package_msgraph.views

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
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)
#ask = Ask(app, "/")

vars = {'date': None, 'time': None, 'duration': None, 'attendees': None}

# since this sample runs locally without HTTPS, disable InsecureRequestWarning
requests.packages.urllib3.disable_warnings()


msgraphapi = oauth.remote_app( \
    'microsoft',
    consumer_key=client_id,
    consumer_secret=client_secret,
    #    request_token_params={'scope': 'User.Read Mail.Send'},
    request_token_params={'scope': 'User.Read Calendars.ReadWrite'},
    base_url='https://graph.microsoft.com/v1.0/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
    authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
)



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


################################################################################################################3


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
    room.token = session['access_token']             # save room token for further useage
    return redirect('main')


@app.route('/main')
def main():
    room.data = cal_data = get_calendars()  # directly load the calenders after login
#    getFreeRooms('2017-08-15T08:00', '2017-08-15T10:00', 7) # directly test the function
    me = get_me()

    """Handler for main route."""
    if session['alias']:
        username = session['alias']
        email_address = session['userEmailAddress']
        return render_template('main.html', name=username, emailAddress=email_address, uID=me['id'], vName=me['givenName'], nName=me['surname'], mail=me['userPrincipalName'], jsondata=cal_data, showCalendars=1)
    else:
        return render_template('main.html', uID=me['id'], vName=me['givenName'], nName=me['surname'], mail=me['userPrincipalName'], jsondata=cal_data, showCalendars=1)


# Get Information about the current account
@app.route('/me')
def get_me():
    me = msgraphapi.get('me')
    return json.loads(json.dumps(me.data))

# Calendars
def get_calendars():
    cal = msgraphapi.get('me/calendars')
    return json.loads(json.dumps(cal.data))


@app.route('/create_calendar')
def create_calendar():
    """Handler for send_mail route."""
    resolveAvailability = request.args.get('resolveAvailability')  # get name of the user the calendar is created for
    city = request.args.get('city')
    countryOrRegion = request.args.get('countryOrRegion')
    postalCode = request.args.get('postalCode')
    state = request.args.get('state')
    street = request.args.get('street')
    displayName = request.args.get('displayName')
    locationEmailAddress = request.args.get('locationEmailAddress')
    maxAttendees = request.args.get('maxAttendees')

    # write new room data to locationConstraint
    create_room_to_json(resolveAvailability, city, countryOrRegion, postalCode, state, street,
                        displayName, locationEmailAddress, maxAttendees)


    response = call_createcalendar_endpoint(session['access_token'], displayName)

    if response == 'SUCCESS':
        show_success = 'true'
        show_error = 'false'
    else:
        print(response)
        show_success = 'false'
        show_error = 'true'

    room.data = get_calendars()

    session['pageRefresh'] = 'true'
    return render_template('main.html', name=session['alias'], username=displayName,
                           showSuccess_createCalendar=show_success, showError_createCalendar=show_error)

@app.route('/delete_calendar')
def delete_calendar():
    me = get_me()
    cal_id = request.args.get('calID')
    calendar_name = request.args.get('calName')
    room.data = None

    response = call_deletecalendar_endpoint(session['access_token'], cal_id)

    errormessage = ''

    if response == 'SUCCESS':
        show_success = 'true'
        show_error = 'false'
    else:
        #print(response.error)
        show_success = 'false'
        show_error = 'true'
        jsonresponse = json.loads(response)
        errormessage = jsonresponse['error']['message']
    return render_template('main.html', name=session['alias'], uID=me['id'], vName=me['givenName'], nName=me['surname'], mail=me['userPrincipalName'],
                           jsondata=room.data, calName=calendar_name, showSuccess_deletedCalendar=show_success, showError_deletedCalendar=show_error, error_deleteCalendar=errormessage, showCalendars=0)


# Events
@app.route('/list_events')
def list_events():
    cal_id = request.args.get('cal_id')
    cal_name = request.args.get('cal_name')
    events = msgraphapi.get('me/calendars/'+cal_id+'/events')
    return render_template('events.html', name=session['alias'], data=events.data, calName=cal_name, jsondata=room.data)


@app.route('/create_event')
def create_event():
    """Handler for create_event route."""
    cal_id = request.args.get('cal_id')
    cal_date = request.args.get('date')
    cal_start_time = request.args.get('start')
    cal_end_time = request.args.get('end')
    cal_title = request.args.get('title')
    cal_room = request.args.get('room')
    start = convert_amazon_to_ms(cal_date, cal_start_time)
    end = convert_amazon_to_ms(cal_date, cal_end_time)
    print("cal id:"+cal_id)
    response = call_createvent_endpoint(session['access_token'], start, end, cal_title, cal_room, cal_id)
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


