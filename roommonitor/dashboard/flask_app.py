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
    # me_response = msgraphapi.get('me')
    # me_data = json.loads(json.dumps(me_response.data))
    # username = me_data['displayName']
    # email_address = me_data['userPrincipalName']
    # session['alias'] = username
    # session['userEmailAddress'] = email_address
    room.token = session['access_token']             # save room token for further usage
    return redirect('main')


@app.route('/main')
def main():
    """
    Main function to display the Dashboard after successful login
    :return: renders Dashboard with all necessary information about the users calenders (rooms) and account information
    """
    room.data = cal_data = get_calendars(session['access_token'])  # directly load the calenders after login
#    getFreeRooms('2017-08-15T08:00', '2017-08-15T10:00', 7) # directly test the function
    me = get_me()
    return render_template('main.html', uID=me['id'], vName=me['givenName'], nName=me['surname'], mail=me['userPrincipalName'], jsondata=cal_data, showCalendars=1)



def get_me():
    """
    Get Information about the current account
    :return: account information about the currently logged in user
    """
    me = msgraphapi.get('me')
    return json.loads(json.dumps(me.data))



### Calendars ###
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
    events = msgraphapi.get('me/calendars/'+cal_id+'/events')
    return render_template('events.html', name=session['alias'], data=events.data, calName=cal_name, jsondata=room.data)


@msgraphapi.tokengetter
def get_token():
    """Return the Oauth token."""
    return session.get('microsoft_token')
