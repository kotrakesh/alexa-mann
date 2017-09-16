##################################################################################
"""
        Main Program including all functionalities from MS Graph and Amazon Alexa
        Other functions are import from other files and packages.

        Developer: Micha (02468), Yide, Arthur, Lev
        Last modified: 2017/09/13
"""
##################################################################################

# import all needed packages and modules
import json
import sys
import uuid
import logging
import requests

from flask     import Flask, redirect, url_for, session, request, render_template
from flask_ask import Ask, statement, question, session as ask_session
from flask_oauthlib.client import OAuth

# import custom modules
from room_class import Room
import util
import ms_endpoints



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
room = Room()

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


@app.route('/')
def index():
    """
    Handler for home page.
    :return: Microsoft login page
    """
    return login()


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
    # me_response = msgraphapi.get('me')
    # me_data = json.loads(json.dumps(me_response.data))
    # username = me_data['displayName']
    # email_address = me_data['userPrincipalName']
    # session['alias'] = username
    # session['userEmailAddress'] = email_address
    room.token = session['access_token']             # save room token for further useage
    return redirect('main')


@app.route('/main')
def main():
    """
    Main function to display the Dashboard after successful login
    :return: renders Dashboard with all necessary information about the users calenders (rooms) and account information
    """
    room.data = cal_data = get_calendars()  # directly load the calenders after login
#    getFreeRooms('2017-08-15T08:00', '2017-08-15T10:00', 7) # directly test the function
    me = get_me()

    if session['alias']:
        username = session['alias']
        email_address = session['userEmailAddress']
        return render_template('main.html', name=username, emailAddress=email_address, uID=me['id'], vName=me['givenName'], nName=me['surname'], mail=me['userPrincipalName'], jsondata=cal_data, showCalendars=1)
    else:
        return render_template('main.html', uID=me['id'], vName=me['givenName'], nName=me['surname'], mail=me['userPrincipalName'], jsondata=cal_data, showCalendars=1)



#@app.route('/me')
def get_me():
    """
    Get Information about the current account
    :return: account information about the currently logged in user
    """
    me = msgraphapi.get('me')
    return json.loads(json.dumps(me.data))



### Calendars ###

def get_calendars():
    """
    Retrieves calendars
    :return: all calendars which belongs to the logged in user
    """
    cal = msgraphapi.get('me/calendars')
    return json.loads(json.dumps(cal.data))



@app.route('/create_calendar')
def create_calendar():
    """
    Creates MS calendar, called by the form on the main page (Dashboard)
    not displayed to the user, used only for internal calls, output is displayed on the Dashboard
    :return: renders Dashboard including a success message upon the creation of the calendar
    """
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

    # write new room data to json database,
    util.create_room_to_json(resolveAvailability, city, countryOrRegion, postalCode, state, street, displayName, locationEmailAddress, maxAttendees)

    # new calendar is created in the Microsoft Account
    response = ms_endpoints.call_createcalendar(session['access_token'], displayName)

    if response == 'SUCCESS':
        show_success = 'true'
        show_error = 'false'
    else:
        print(response)
        show_success = 'false'
        show_error = 'true'

    room.data = get_calendars()

    session['pageRefresh'] = 'true'
    # returns Dashboard
    return render_template('main.html', name=session['alias'], username=displayName,
                           showSuccess_createCalendar=show_success, showError_createCalendar=show_error)


@app.route('/delete_calendar')
def delete_calendar():
    """
    Deletes MS calendar, called by the form on the main page (Dashboard)
    not displayed to the user, used only for internal calls, output is displayed on the Dashboard
    :return: renders Dashboard including a success message upon the deletion of the calendar
    """
    me = get_me()
    cal_id = request.args.get('calID')
    calendar_name = request.args.get('calName')

    room.data = None

    response = ms_endpoints.call_deletecalendar(session['access_token'], cal_id)
    util.delete_room_to_json(calendar_name)

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
    #return Dashboard
    return render_template('main.html', name=session['alias'], uID=me['id'], vName=me['givenName'], nName=me['surname'], mail=me['userPrincipalName'],
                           jsondata=room.data, calName=calendar_name, showSuccess_deletedCalendar=show_success, showError_deletedCalendar=show_error, error_deleteCalendar=errormessage, showCalendars=0)


### Events ###
@app.route('/list_events')
def list_events():
    """
    Ajax function for retrieving events per calendar
    :return:  template of events which is asynchronously loaded into the Dashboard
    """
    cal_id = request.args.get('cal_id')
    cal_name = request.args.get('cal_name')
    events = msgraphapi.get('me/calendars/'+cal_id+'/events')
    return render_template('events.html', name=session['alias'], data=events.data, calName=cal_name, jsondata=room.data)

# # still necessary?
# @app.route('/create_event')
# def create_event():
#     """Handler for create_event route."""
#     cal_id = request.args.get('cal_id')
#     cal_date = request.args.get('date')
#     cal_start_time = request.args.get('start')
#     cal_end_time = request.args.get('end')
#     cal_title = request.args.get('title')
#     cal_room = request.args.get('room')
#     start = util.convert_amazon_to_ms(cal_date, cal_start_time)
#     end = util.convert_amazon_to_ms(cal_date, cal_end_time)
#     print("cal id:"+cal_id)
#     response = ms_endpoints.call_createvent(session['access_token'], start, end, cal_title, cal_room, cal_id)
#     if response == 'SUCCESS':
#         show_success = 'true'
#         show_error = 'false'
#     else:
#         print(response)
#         show_success = 'false'
#         show_error = 'true'
#
#     session['pageRefresh'] = 'false'
#     return render_template('main.html', name=session['alias'], data=response, showSuccess=show_success,
#                            showError=show_error)

#still needed??
# @app.route('/list_events_for_time')
# def list_events_for_time():
#     cal_id = request.args.get('cal_id')  # get email address from the form
#     cal_name = request.args.get('cal_name')
#     cal_date = request.args.get('date')
#     cal_start_time = request.args.get('start_time')
#     cal_end_time = request.args.get('end_time')
#     start = util.convert_amazon_to_ms(cal_date, cal_start_time)
#     end = util.convert_amazon_to_ms(cal_date, cal_end_time)
#     response = ms_endpoints.call_listevents_for_time(session['access_token'], cal_id, start, end)
#     data = json.loads(response.text)
#
#     print(cal_name, cal_date, cal_start_time, cal_end_time)
#     if response.ok:
#         show_success = 'true'
#         show_error = 'false'
#     else:
#         print(response)
#         show_success = 'false'
#         show_error = 'true'
#
#     session['pageRefresh'] = 'false'
#     #print(response)
#
#     return render_template('calendars.html', name=session['alias'], calName=cal_name, data=data,
#                            showSuccess_listEvents=show_success, showError_listEvents=show_error, showEvents=1)


@msgraphapi.tokengetter
def get_token():
    """Return the Oauth token."""
    return session.get('microsoft_token')


################################################################################################################3

# Alexa Skill Part

@ask.launch
def welcome():
    """
    A launch function invoked at the beginnning when user starts Alexa (LaunchIntent)
    :return: Hello, please tell me the dates and times when your meeting shall be scheduled
    """
    room.date = None  # '2017-07-16'
    room.time = None  # '03:00'
    room.duration = None  # 'PT5M'
    return question(render_template('msg_launch_request'))


@ask.intent("DateIntent")
def missing_duration_time(Date):
    """
    Function called when user specifies the date only
    :param Date:    date of the event
    :return:        What time is the meeting and how long is it?
    """
    room.date = Date

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
    """
    Function called when user specifies the time only
    :param Time:    time of the event
    :return:        Whats the date and the duration of the meeting?
    """
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
    """
    Function called when user specifies the duration only
    :param Duration:    duration of the event
    :return:            What day and what time is the meeting?
    """
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
    """
    Function called when user specifies date and duration
    :param Date:        date of the event
    :param Duration:    duration of the event
    :return:            What time is the meeting?
    """
    room.date = Date
    room.duration = Duration

    if not room.time:
        return question(render_template('msg_missing_time'))
    else:
        return allKnown(room.date, room.time, room.duration)


@ask.intent("DateTimeIntent")
def missing_duration(Date, Time):
    """
    Function called when user specifies date and time
    :param Date:    date of the event
    :param Time:    time of the event
    :return:        How long is the meeting?
    """
    room.date = Date
    room.time = Time

    if not room.duration:
        print('DateTimeIntent no duration')
        return question(render_template('msg_missing_duration'))
    else:
        return allKnown(room.date, room.time, room.duration)


@ask.intent("TimeDurationIntent")
def missing_date(Time, Duration):
    """
    Function called when user specifies time and duration
    :param Time:        time of the event
    :param Duration:    duration of the event
    :return:            What day is the meeting?
    """
    room.duration = Duration
    room.time = Time
    if not room.date:
        return question(render_template('msg_missing_date'))
    else:
        return allKnown(room.date, room.time, room.duration)


@ask.intent("DataTimeDurationIntent")
def allKnown(Date, Time, Duration):
    """
    Function called when user specifies the date, time and duration
    :param Date:        date of the event
    :param Time:        time of the event
    :param Duration:    duration of the event
    :return:            How many attendees will attend the meeting?
    """
    room.date = Date
    room.time = Time
    room.duration = Duration
    print('DataTimeDurationIntent ' + str(Date), str(Time), str(Duration))

    return question(render_template('msg_attendees'))


@ask.intent("AttendeesIntent")
def numberOfAttendees(Attendees):
    """
    Function called when the user specifies the number of attendees
    :param Attendees:   number of attendees who will attend the meeting
    :return:            Whats the title of the event?
    """
    room.attendees = Attendees
    if not room.duration or not room.date or not room.time:
        return question("Please, specify the date, time and the duration first")
    #TODO specify missing information
    return question(render_template('msg_title'))


@ask.intent("TitleIntent")
def title_of_event(Title):
    """
    Function called when user specifies the title of the event
    :param Title:   title of the event
    :return:        readMeeetingTime(date, time, duration, attendees, title)
    """
    if room.date and not room.time and room.duration:
        return missing_time(room.date, room.duration)
    if not room.date and room.time and room.duration:
        return missing_date(room.time, room.duration)
    if room.date and room.time and not room.duration:
        return missing_duration(room.date, room.time)
    else:
        return readMeetingTime(room.date, room.time, room.duration, room.attendees, Title)



def readMeetingTime(Date, Time, Duration, Attendees, Title):
    """
    Function which initialized the room search and room booking
    :param Date:        date of the event
    :param Time:        time of the event
    :param Duration:    duration of the event
    :param Attendees:   number of attendees at the event
    :param Title:       title of the event
    :return:            statement for Amazon Echo including card information
    """
    print('readMeetingTime')
    ask_session.attributes['date'] = ask_session.attributes['time'] = ask_session.attributes['duration'] = room.date = room.time = room.duration = None

    # Changing datatypes for Microsoft
    start = util.convert_amazon_to_ms(Date, Time)
    # calculate: end = start_time + duration
    am_end = util.getMeetingEndTime(Time, Duration)
    end = util.convert_amazon_to_ms(Date, am_end)

    # check for free rooms with the constraints
    result = getFreeRooms(start, end, Attendees, Title)

    if (result['roomFound'] == 1):
        # returns answer to Alexa and displays the card in the Alexa App, at this time the calendar event already has been booked
        return statement(render_template('msg_booked_room_success', roomname=result['roomName']))\
            .simple_card(title=render_template('card_booked_room_success_title'), content= render_template('card_booked_room_success_content', roomname=result['roomName'], start=start, end=end, attendees=Attendees))
    else:
        # Alexa gets informed about the failed booking, in some cases the fail reason is send and also displayed on the Alexa Card
        return statement(render_template('msg_booked_room_fail', fail_reason=result['reason']))\
            .simple_card(title=render_template('card_booked_room_fail_title'), content=render_template('card_booked_room_fail_content', fail_reason=result['reason']))




def getFreeRooms(t_start, t_end, attendees, title):
    """
    Searches for free rooms with the given constraints of start, end and number of attendees
        First loop: iterate through the Microsoft Calendars to find rooms
        Second loop: iterate through the json database to check the number of attendees constraint as this value can't be saved in the Microsoft calendar

    :param t_start:     start of the event
    :param t_end:       end of the event
    :param attendees:   number of people attending the meeting (room constraint)
    :param title:       title of the event
    :return:            python object, with information about status of room booking and fail reason on error
    """
    # TODO authenticate with Graph API

    print(str(t_start), str(t_end), ' Attendees: ', str(attendees), ' ', str(title), ' --- cal.data: ')

    # opens the json database
    locConstraint = json.load(open('./resources/locationConstraint.json'))

    # Workaround to load rooms from Microsoft, User MUST login in on the portal before
    if(room.data is None):
        return {'roomFound': 0, 'roomName': '', 'reason': 'Error while loading rooms from Microsoft API'}


    for cal in room.data['value']:
        # ignore some standard calendars
        if (cal['name'] == 'Calendar' or cal['name'] == 'Birthdays' or cal['name'] == 'Room 3'):
            continue

        print(' ------------ ')
        print('name: ' + str(cal['name']))

        #returns events for the specified times
        jdata = ms_endpoints.call_listevents_for_time(room.token, cal['id'], t_start, t_end)
        data = json.loads(jdata.text)

        if not data['value']:
            # first constraint passed: no events are listed in that calendar for those times: data['value'] array is empty
            print('Keine Events vorhanden')

            # second constraint: load rooms from the local database, often the main error source as localdatabase is not updated
            for l in locConstraint['locations']:

                if l['displayName'] == cal['name']:
                    # check if the room is big enough to hold the number of specified people
                    if int(attendees) <= int(l['maxAttendees']):
                        print('Raumgroesse: ' +  str(attendees), ' max: ', str(l['maxAttendees']))
                        print('Das Meeting findet in Raum ' + cal['name'] + ' statt!')
                        print('    ')

                        # create calendar event for that room
                        util.create_event_from_alexa(t_start, t_end, title, cal['name'], cal['id'])

                        # Free room found
                        return {'roomFound': 1, 'roomName': cal['name'], 'reason': ''}
                    else:
                        # room is too small, look for the next room
                        print('Raumgroesse: ' + str(attendees), ' > ', str(l['maxAttendees']))
                        print('Raum ist zu klein')

        else:
            print('Events vorhanden')
    return {'roomFound': 0, 'roomName': cal['name'], 'reason': 'No free room was found'}

