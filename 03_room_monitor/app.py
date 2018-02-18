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
    room.token = session['access_token']             # save room token for further usage
    return redirect('main')


@app.route('/main')
def main():
    """
    Main function to display the Dashboard after successful login
    :return: renders Dashboard with all necessary information about the users calenders (rooms) and account information
    """

    room.data = cal_data = get_calendars(session['access_token'])  # directly load the calenders after login
    me = get_me()
    locationConstraint = util.load_locationConstraint()

    return render_template('main.html', uID=me['id'], vName=me['givenName'], nName=me['surname'], mail=me['userPrincipalName'],
                               jsondata=cal_data, showCalendars=1, locConstraint=locationConstraint)



#@app.route('/me')
def get_me():
    """
    Get Information about the current account
    :return: account information about the currently logged in user
    """
    me = msgraphapi.get('me')
    return json.loads(json.dumps(me.data))



### Calendars ###
# TODO check if token is set
def get_calendars(token):
    """
    Retrieves calendars
    :param:  session token to authenticate with Microsoft, used by Amazon as well
    :return: all calendars which belongs to the logged in user
    """
    cal = ms_endpoints.call_getcalendars(token)
    print('cal: ')
    print(cal)
    #convert to json
    cal_json = json.loads(cal)
    print('cal_json')
    print(cal_json)
    return cal_json


# USED only for the MS Frontend
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

    room.data = get_calendars(session['access_token'])

    session['pageRefresh'] = 'true'
    # returns Dashboard
    me = get_me()
    return render_template('main.html', name=session['alias'], uID=me['id'], vName=me['givenName'], nName=me['surname'], mail=me['userPrincipalName'],
                           showSuccess_createCalendar=show_success, showError_createCalendar=show_error)

# USED only for the MS Frontend
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
    #TODO not working yet
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


# USED only for the MS Frontend
### Events ###
@app.route('/list_events')
def list_events():
    """
    Ajax function for retrieving events per calendar
    :return:  template of events which is asynchronously loaded into the Dashboard
    """
    cal_id = request.args.get('cal_id')
    cal_name = request.args.get('cal_name')
    #events = msgraphapi.get('me/calendars/'+cal_id+'/events')
    events = json.loads(ms_endpoints.call_listevents(session['access_token'], cal_id).text)
    return render_template('events.html', name=session['alias'], data=events, calName=cal_name, jsondata=room.data)


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
    room.roomNumber = None
    room.bookingProcess = 1
    return checkAccessToken(question(render_template('msg_launch_request')))

    # return question(render_template('msg_launch_request'))

# Built-in intents
@ask.intent("AMAZON.HelpIntent")
def intent_help():
    return question(render_template('msg_help'))

@ask.intent("AMAZON.CancelIntent")
def intent_cancel():
    room.date = room.title = room.duration = room.attendees = room.title = room.roomNumber = None #delete all values
    return statement(render_template('msg_bye'))

@ask.intent("AMAZON.StopIntent")
def intent_stop():
    room.date = room.title = room.duration = room.attendees = room.title = room.roomNumber = None #delete all values
    return statement(render_template('msg_bye'))

@ask.session_ended
def session_ended():
    room.date = room.title = room.duration = room.attendees = room.title = room.roomNumber = None #delete all values
    return "{}", 200


@ask.intent("AMAZON.NoIntent")
def intent_no():
    room.date = room.time = room.roomNumber = room.duration = None
    return statement(render_template('msg_no'))

# invoked after user is asked if he wants to book the room
@ask.intent("AMAZON.YesIntent")
def intent_yes():
    print('yes intent ---')
    room.bookingProcess = 1
    room.duration = "PT1H"
    return question(render_template('msg_attendees'))

# Custom intents
@ask.intent("DateIntent")
def missing_duration_time(Date):
    """
    Function called when user specifies the date only
    :param Date:    date of the event
    :return:        What time is the meeting and how long is it?
    """
    room.date = Date
    return checkAccessToken(checkMissingAttributes_Phase1())


@ask.intent("TimeIntent")
def missing_date_duration(Time):
    """
    Function called when user specifies the time only
    :param Time:    time of the event
    :return:        Whats the date and the duration of the meeting?
    """
    room.time = Time
    return checkAccessToken(checkMissingAttributes_Phase1())


@ask.intent("DurationIntent")
def missing_date_time(Duration):
    """
    Function called when user specifies the duration only
    :param Duration:    duration of the event
    :return:            What day and what time is the meeting?
    """
    room.duration = Duration
    return checkAccessToken(checkMissingAttributes_Phase1())


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
    return checkAccessToken(checkMissingAttributes_Phase1())


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
    return checkAccessToken(checkMissingAttributes_Phase1())


@ask.intent("TimeDurationIntent")
def missing_date(Time, Duration):
    """
    Function called when user specifies time and duration
    :param Time:        time of the event
    :param Duration:    duration of the event
    :return:            What day is the meeting?
    """
    room.time = Time
    room.duration = Duration
    return checkAccessToken(checkMissingAttributes_Phase1())


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
    return checkAccessToken(checkMissingAttributes_Phase1())



@ask.intent("AttendeesIntent")
def numberOfAttendees(Attendees):
    """
    Function called when the user specifies the number of attendees
    :param Attendees:   number of attendees who will attend the meeting
    :return:            Whats the title of the event?
    """
    room.attendees = Attendees
    checkMissingAttributes_Phase1()

    # check if Attendees is really a valid number, Problem: also invoked if title intent is misused
    # try:
    #     isinstance(int(Attendees), int)
    # except:
    #     return question(render_template('msg_NaN'))

    if Attendees is None:
        return question(render_template('msg_attendees'))
    else:
        return question(render_template('msg_title'))


@ask.intent("TitleIntent")
def title_of_event(Title):
    """
    Function called when user specifies the title of the event
    :param Title:   title of the event
    :return:        readMeeetingTime(date, time, duration, attendees, title)
    """
    room.title = Title
    if Title is None:
        return question(render_template('msg_title'))
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

    ask_session.attributes['date'] = ask_session.attributes['time'] = ask_session.attributes['duration'] = room.date = room.time = room.duration = None

    # Changing datatypes for Microsoft
    print('Time of the event:')
    print(Time, Duration)

    # check for free rooms with the constraints, after room was checked
    if room.roomNumber is not None:
        result = getFreeRooms(Date, Time, Duration, Attendees, Title, room.roomNumber)
    else:
        room.roomNumber = None
        result = getFreeRooms(Date, Time, Duration, Attendees, Title, None)

    print(result)

    # Result from getFreeRooms, either positive or negative regarding free rooms, if negative error message is provided
    if (result['roomFound'] == 1):
        # returns answer to Alexa and displays the card in the Alexa App, at this time the calendar event already has been booked
        return statement(render_template('msg_booked_room_success', roomname=result['roomName']))\
            .simple_card(title=render_template('card_booked_room_success_title'), content= render_template('card_booked_room_success_content', roomname=result['roomName'], start=Time, duration=Duration, attendees=Attendees))
    else:
        # Alexa gets informed about the failed booking, in some cases the fail reason is send and also displayed on the Alexa Card
        return statement(render_template('msg_booked_room_fail', fail_reason=result['reason']))\
            .simple_card(title=render_template('card_booked_room_fail_title'), content=render_template('card_booked_room_fail_content', fail_reason=result['reason']))



def getFreeRooms(Date, Time, Duration, attendees, title, roomnumber):
    """
    Searches for free rooms with the given constraints of start, end and number of attendees
        First loop: iterate through the Microsoft Calendars to find rooms
        Second loop: iterate through the json database to check the number of attendees constraint as this value can't be saved in the Microsoft calendar

    :param Date:        start of the event in Amazon format
    :param Time:        end of the event in Amazon Format
    :param Duration:    duration of the event in Amazon format
    :param attendees:   number of people attending the meeting (room constraint)
    :param title:       title of the event
    :return:            python object, with information about status of room booking and fail reason on error
    """
    print('getFreeRooms')
    room_name = 'Meetingroom ' + str(roomnumber)

    # List Time and creating time are different due to different time zones and support of the MS API
    start_listevents   = util.convert_amazon_to_ms(Date, util.timeSum(Time, "22:00"))
    start_createevents = util.convert_amazon_to_ms(Date, Time)

    # calculate: end = start_time + duration
    end_listevents   = util.getMeetingEndTimeMinusTwoH(Time, Duration)
    end_createevents = util.getMeetingEndTime(Time, Duration)
    end_listevents   = util.convert_amazon_to_ms(Date, end_listevents)
    end_createevents = util.convert_amazon_to_ms(Date, end_createevents)

    if end_listevents == -1 or end_createevents == -1:
        fail_end_time = 'End time could not be calculated'
        return statement(render_template('msg_booked_room_fail', fail_reason=fail_end_time)) \
            .simple_card(title=render_template('card_booked_room_fail_title'),
                         content=render_template('card_booked_room_fail_content', fail_reason=fail_end_time)
                         )


    print('start and endtimes: ', start_listevents, start_createevents, end_listevents, end_createevents)
    print(' Attendees: ', str(attendees), ', ', str(title))

    # opens the json database
    locConstraint = util.load_locationConstraint()
    room.data = get_calendars(room.token)

    if(room.data is None):
        return {'roomFound': 0, 'roomName': '', 'reason': 'Error while loading rooms from Microsoft API'}

    for cal in room.data['value']:
        # ignore some standard calendars
        if (cal['name'] == 'Calendar' or cal['name'] == 'Birthdays' or cal['name'] == 'Room 3'):
            continue

        # if room has been specified
        if cal['name'] == room_name:
            print('specified room found: ' + room_name)
            for l in locConstraint['locations']:

                if l['displayName'] == room_name:
                    # check if the room is big enough to hold the number of specified people
                    if int(attendees) <= int(l['maxAttendees']):
                        print('Anzahl Teilnehmer: ' + str(attendees), ' max Raumgroesse: ', str(l['maxAttendees']))
                        print('Das Meeting findet in Raum ' + cal['name'] + ' statt!')
                        print('    ')

                        # create calendar event for that room
                        ms_endpoints.call_createvent(room.token, start_createevents, end_createevents, title, cal['name'], cal['id'])
                        # Free room found
                        return {'roomFound': 1, 'roomName': cal['name'], 'reason': ''}
                    else:
                        # room is too small, look for the next room
                        print('Raumgroesse: ' + str(attendees), ' > ', str(l['maxAttendees']))
                        print('Raum ist zu klein')

            return {'roomFound': 0, 'roomName': cal['name'], 'reason': 'Room is too small for this amount of people'}


        #returns events for the specified times
        jdata = ms_endpoints.call_listevents_for_time(room.token, cal['id'], start_listevents, end_listevents)
        data = json.loads(jdata.text)
        print(jdata.text)

        if not data['value']:
            # first constraint passed: no events are listed in that calendar for those times: data['value'] array is empty
            print('- Keine Events vorhanden in ' + str(cal['name']))

            # second constraint: load rooms from the local database, often the main error source as localdatabase is not updated
            for l in locConstraint['locations']:
                print('- current locationConstraintCheck: ' + str(l['displayName']))
                if l['displayName'] == cal['name']:
                    # check if the room is big enough to hold the number of specified people
                    if int(attendees) <= int(l['maxAttendees']):
                        print('Anzahl Teilnehmer: ' +  str(attendees), ' max Raumgroesse: ', str(l['maxAttendees']))
                        print('Das Meeting findet in Raum ' + cal['name'] + ' statt!')
                        print('    ')

                        # create calendar event for that room
                        ms_endpoints.call_createvent(room.token, start_createevents, end_createevents, title, cal['name'], cal['id'])
                        # Free room found
                        return {'roomFound': 1, 'roomName': cal['name'], 'reason': ''}
                    else:
                        # room is too small, look for the next room
                        print('Raumgroesse: ' + str(attendees), ' > ', str(l['maxAttendees']))
                        print('Raum ist zu klein')

        else:
            print('Events vorhanden in room ', cal['name'], ' ', room.data['value'])
        print(' ------------ ')
    return {'roomFound': 0, 'roomName': cal['name'], 'reason': 'No free room was found'}


### New Skill
@ask.intent("GetAllRoomsIntent")
def getAllMeetingRooms():
    """
       Alexa names all rooms in the office which can be used for a meeting
    """
    roomNames = ""
    try:
        room.token = ask_session['user']['accessToken']  # get the MS Token from the Alexa Session after successful account linking
    except:
        print('room token was not set')
        return statement('The MS Graph Token couldn\'t be accessed. Please link your account!').link_account_card()

    try:
        room.data = get_calendars(room.token)
    except:
        return statement(render_template('msg_check_room_fail'))

    for cal in room.data['value']:
        if (cal['name'] == 'Calendar' or cal['name'] == 'Birthdays' or cal['name'] == 'Room 3'):
            continue
        roomName = cal['name'] + ", "
        roomNames += roomName
    print(roomNames)
    return statement(render_template('msg_check_room_success', roomnames=roomNames))




# is room 2 available
# @ask.intent("RoomAvailabilityDateIntent")
# @ask.intent("RoomIntent")
# num as parameter
@ask.intent("RoomAvailabilityIntent")
def checkRoomAvailableDate(Room):
    '''
    Skill: Check availability of rooms
    :param Room: Number of room (integer)
    :return: check access token, if set call checkMissingAttributes for the room check
    '''
    print('room available?')
    room.bookingProcess = 0
    room.roomNumber = Room
    return checkAccessToken(checkMissingAttributes_RoomAvailable(Room))


# is room 2 available tomorrow
@ask.intent("RoomAvailabilityDateIntent")
def checkRoomAvailableDate(Room, Date):
    '''
    Skill:
    :param Room:
    :param Date:
    :return:
    '''
    print('room available?')
    room.date = Date
    room.bookingProcess = 0
    room.roomNumber = Room
    return checkAccessToken(checkMissingAttributes_RoomAvailable(Room))


# is room 2 available at 2 pm
@ask.intent("RoomAvailabilityTimeIntent")
def checkRoomAvailableTime(Room, Time):
    print('room available?')
    room.time = Time
    room.bookingProcess = 0
    room.roomNumber = Room
    return checkAccessToken(checkMissingAttributes_RoomAvailable(Room))


###
@ask.intent("RoomAvailabilityDateTimeIntent")
def checkRoomAvailable(Date, Time, Room):
    """
       check whether a specific room is still available for a time

       :param Date:
       :param Time:
       :param Duration:
       :param Room_:   Number of the room
       """
    try:
        room.token = ask_session['user']['accessToken']  # get the MS Token from the Alexa Session after successful account linking
    except:
        print('room token was not set')
        return statement('The MS Graph Token couldn\'t be accessed. Please link your account!').link_account_card()


    room_name = 'Meetingroom '+ str(Room)
    room.date = Date
    room.time = Time
    room.bookingProcess = 0
    room.roomNumber = Room

    # Changing datatypes for Microsoft
    start = util.convert_amazon_to_ms(Date, util.timeSum(Time, "22:00"))

    # calculate: end = start_time + duration
    am_end = util.getMeetingEndTimeMinusTwoH(Time, "PT1H")
    end = util.convert_amazon_to_ms(Date, am_end)


    print('room name: '+ room_name)
    room.data = get_calendars(room.token)

    if (room.data is None):
        result = {'roomFound': False, 'roomAvailable': False, 'roomName': '', 'roomId': '', 'reason': 'Error while loading rooms from Microsoft API'}
    else:
        for cal in room.data['value']:
            # ignore some standard calendars
            print('check Available with '+cal['name'])
            if (cal['name'] == room_name):
                print("found room "+ room_name)
                # check whether this room is free at that time.
                print('start and endtimes: ', start, ' ', end)
                jdata = ms_endpoints.call_listevents_for_time(room.token, cal['id'], start, end)
                print(jdata.text)
                data = json.loads(jdata.text)

                if not data['value']:
                    # first constraint passed: no events are listed in that calendar for those times: data['value'] array is empty
                    print('Keine Events vorhanden')
                    result = {'roomFound': True, 'roomAvailable': True, 'roomName': cal['name'], 'roomId': cal['id'], 'reason': 'no event in this room'}
                else:
                    result = {'roomFound': True, 'roomAvailable': False, 'roomName': cal['name'], 'roomId': '', 'reason': data['value'][0]['subject']}
                break
            else:
                print("no name match")
                result = {'roomFound': False, 'roomAvailable': False, 'roomName': cal['name'], 'roomId': '', 'reason': 'cannot find this room' + room_name}

    # check for free rooms with the constraints
    print(result)


    if (result['roomFound'] == True and result['roomAvailable'] == True):
        # returns answer to Alexa and displays the card in the Alexa App, at this time the calendar event already has been booked
        print('room has been found and is available')
        return question(render_template('msg_availableRoom', roomname=result['roomName']))

    if (result['roomFound'] == True and result ['roomAvailable']== False):
        room.roomNumber = room.date = room.time = None  # reset all values before further actions
        # Alexa gets informed about the failed booking, in some cases the fail reason is send and also displayed on the Alexa Card
        return statement(render_template('msg_notAvailableRoom', roomname=result['roomName'], eventlists=result['reason'])) \
            .simple_card(title=render_template('card_booked_room_fail_title'),
                         content=render_template('card_booked_room_fail_content', fail_reason=result['reason']))

    if (result['roomFound'] == False):
        room.roomNumber = room.date = room.time = None  # reset all values before further actions
        return statement(render_template('msg_booked_room_fail', fail_reason=result['reason'])) \
            .simple_card(title=render_template('card_booked_room_fail_title'),
                         content=render_template('card_booked_room_fail_content', fail_reason=result['reason']))


@ask.intent('EventIntent')
def checkEventsForRoom(date, room_name):
    """
       Get all events from a room for the whole day
       :param date: date when the events take place
       :param room_name:   name of the room
       """
    timeData = util.getAllDayHours(date)
    t_start = timeData['start_time']
    t_end = timeData['end_time']
    print('getAllRooms')
    room.data = get_calendars(room.token)

    if (room.data is None):
        return {'roomFound': False, 'roomName': '', 'roomId': '', 'eventlist': '',
                'reason': 'Error while loading rooms from Microsoft API'}
    for cal in room.data['value']:
        if (cal['name'] == room_name):
            print("find this room" + room_name)
            # check whether this room is free at that time.
            jdata = ms_endpoints.call_listevents_for_time(room.token, cal['id'], t_start, t_end)
            print(jdata.text)
            data = json.loads(jdata.text)
            if not data['value']:
                # first constraint passed: no events are listed in that calendar for those times: data['value'] array is empty
                print('Keine Events vorhanden')
                return {'roomFound': True, 'roomName': cal['name'], 'roomId': cal['id'], 'eventlist': '',
                        'reason': 'No event for this time'}
            else:
                {'roomFound': True, 'roomName': cal['name'], 'roomId': cal['id'], 'eventlist': data['value'],
                 'reason': ''}
    return {'roomFound': False, 'roomName': '', 'roomId': '', 'eventlist': '', 'reason': 'cannot find this room'}


### UTIL ###
# only with parameter function
def checkAccessToken(function):
    try:
        room.token = ask_session['user']['accessToken']  # get the MS Token from the Alexa Session after successful account linking
        return function
    except:
        print('room token was not set')
        return statement('The MS Graph Token couldn\'t be accessed. Please link your account!').link_account_card()


# Tests for missing attributes
def checkMissingAttributes_Phase1(): # date time duration                               # d t d
    if room.bookingProcess == 0:
        print('no room is booked now')
        return checkMissingAttributes_RoomAvailable(room.roomNumber)
    else:
        print('###### check missing attributes ########')
        print('-- attributes - date: ', room.date, ', time:', room.time, ' dur:', room.duration)
        if room.date is None and room.time is None and room.duration is None:               # 0 0 0
            return question(render_template(('msg_missing_date_time_duration')))
        if room.date is None and room.time is None and room.duration is not None:           # 0 0 1
            return question(render_template(('msg_missing_date_time')))
        if room.date is None and room.time is not None and room.duration is None:           # 0 1 0
            return question(render_template(('msg_missing_date_duration')))
        if room.date is None and room.time is not None and room.duration is not None:       # 0 1 1
            return question(render_template(('msg_missing_date')))
        if room.date is not None and room.time is None and room.duration is None:           # 1 0 0
            return question(render_template(('msg_missing_time_duration')))
        if room.date is not None and room.time is None and room.duration is not None:       # 1 0 1
            return question(render_template(('msg_missing_time')))
        if room.date is not None and room.time is not None and room.duration is None:       # 1 1 0
            return question(render_template(('msg_missing_duration')))
        if room.date is not None and room.time is not None and room.duration is not None:   # 1 1 1
            return question(render_template('msg_attendees'))

def checkMissingAttributes_RoomAvailable(Room):  # date time          # d t
    print('###### check missing attributes room available ########')
    if Room is None:
        room.roomNumber = room.date = room.time = room.duration = room.attendees = None  # reset all values before further actions
        room.bookingProcess = 1
        return question(render_template('msg_missing_date_time_duration'))

    if room.date is None and room.time is None:                       # 0 0
        return question(render_template(('msg_booking_date_time')))

    if room.date is None and room.time is not None:                   # 0 1
        return question(render_template(('msg_booking_date')))

    if room.date is not None and room.time is None:                   # 1 0
        print('missing time')
        return question(render_template(('msg_booking_time')))

    if room.date is not None and room.time is not None:               # 1 1
        print('all data is available')
        return checkRoomAvailable(room.date, room.time, Room)



###nur for test
@app.route('/check_ava')
def testFunc():
    data = checkRoomAvailable("2017-10-07T15:00:00", "2017-10-07T15:30:00", "Room 1")
    print(data['roomAvailable'])

if __name__ == '__main__':
	app.run(host='ghk3pcg5q0.execute-api.us-east-1.amazonaws.com/dev', port=443) # for deployment on lambda
	# app.run()								     # for local testing
