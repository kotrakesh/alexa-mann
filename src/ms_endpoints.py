import requests
import uuid
import json

### Events
def call_createvent(access_token, tStart, tEnd, title, roomName, cal_id):
    '''
    Creates an event in the outlook calendar with the given parameters
    :param access_token: Security token for the MS Graph API
    :param tStart: Start time of the event
    :param tEnd: End time of the event
    :param title: Title of the event
    :param roomName: Name of the room, displayed as location in the Outlook Calendar
    :param cal_id: ID of the calendar the events are searched in
    :return: list of events. On error the status code and error message are returned
    '''
    send_event_url = 'https://graph.microsoft.com/v1.0/me/calendars/'+cal_id+'/events'

    # set request headers
    headers = {'User-Agent': 'python_tutorial/1.0',
               'Authorization': 'Bearer {0}'.format(access_token),
               'Accept': 'application/json',
               'Content-Type': 'application/json'
               }

    request_id = str(uuid.uuid4())
    instrumentation = {'client-request-id': request_id,
                       'return-client-request-id': 'true'}
    headers.update(instrumentation)

    # Building the event JSON File, contains all information which is later displayed in the event and can be viewed in Outlook
    event = {
        "subject": title,
        "body": {
            "contentType": "HTML",
            "content": ""
        },
        "start": {
            "dateTime": tStart,
            "timeZone": "W. Europe Standard Time"
        },
        "end": {
            "dateTime": tEnd,
            "timeZone": "W. Europe Standard Time"
        },
        "location": {
            "displayName": roomName
        }
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


def call_listevents(access_token, id):
    '''
    This function returns an array of events
    :param access_token: Security token for the MS Graph API
    :param id: ID of the calendar the events are searched in
    :return: list of events. On error the status code and error message are returned
    '''
    #GET /me/calendars/{id}/events
    list_events_url = 'https://graph.microsoft.com/v1.0/me/calendars/' + id + '/events'

    # set request headers
    headers = {'User-Agent': 'python_tutorial/1.0',
               'Authorization': 'Bearer {0}'.format(access_token),
               'Accept': 'application/json',
               'Content-Type': 'application/json',
               'Prefer' : 'outlook.timezone="W. Europe Standard Time"'
               }

    request_id = str(uuid.uuid4())
    instrumentation = {'client-request-id': request_id,
                       'return-client-request-id': 'true'}
    headers.update(instrumentation)

    response = requests.get(url=list_events_url,
                            headers=headers,
                            verify=False,
                            params=None)
    print(response)
    if response.ok:
        return response
    else:
        print('ms listevents failed !!!!!')
        #TODO try and exception
        return '{0}: {1}'.format(response.status_code, response.text)

def call_listevents_for_time(access_token, id, start, end):
    '''
    This function returns an array of events for the specified times
    :param access_token: Security token for the MS Graph API
    :param id: ID of the calendar the events are searched in
    :param start: Start time of the event
    :param end: End time of the event
    :return: list of events. On error the status code and error message are returned
    '''
    list_events_url = 'https://graph.microsoft.com/v1.0/me/calendars/' + id + '/calendarView?startDateTime=' + start + 'Z&endDateTime=' + end + 'Z'

    # set request headers
    headers = {'User-Agent': 'python_tutorial/1.0',
               'Authorization': 'Bearer {0}'.format(access_token),
               'Accept': 'application/json',
               'Content-Type': 'application/json',
               'Prefer' : 'outlook.timezone="W. Europe Standard Time"'
               }

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
        print('ms listevents failed !!!!!')
        #TODO try and exception
        return '{0}: {1}'.format(response.status_code, response.text)



### Calendars

def call_getcalendars(access_token):
    '''
    Retrieves all calendars (rooms)
    :param access_token: Security token for the MS Graph API
    :return: list of all calendars stored for the logged in Microsoft account
    '''
    send_calendar_url = 'https://graph.microsoft.com/v1.0/me/calendars'

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
        return response.text # make sure to return the text attribute instead of the full object
    else:
        print('error: ')
        return '{0}: {1}'.format(response.status_code, response.text)



def call_createcalendar(access_token, name):
    '''
    This function creates a new calendar in the Office Account
    :param access_token: Security token for the MS Graph API
    :param name: Name of the calendar as it is displayed in Outlook
    :return: Success or error message on fail
    '''
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

    # parses the user_data as json to enrich the calendar information
    response = requests.post(url=create_calendar_url,
                             headers=headers,
                             data=json.dumps(user_data),
                             verify=False,
                             params=None)

    if response.ok:
        return 'SUCCESS'
    else:
        return '{0}: {1}'.format(response.status_code, response.text)


def call_deletecalendar(access_token, id):
    '''
    This function deletes a calendar in the Office Account
    Upon deletion all events in the respective calendar will be lost
    :param access_token:  Security token for the MS Graph API
    :param id:  ID of the calender to be deleted
    :return: Success or error message on fail
    '''
    send_calendar_url = 'https://graph.microsoft.com/v1.0/me/calendars/'+id

    # set request headers
    headers = {'User-Agent': 'python_tutorial/1.0',
               'Authorization': 'Bearer {0}'.format(access_token),
               'Accept': 'application/json',
               'Content-Type': 'application/json'}

    request_id = str(uuid.uuid4())
    instrumentation = {'client-request-id': request_id,
                       'return-client-request-id': 'true'}
    headers.update(instrumentation)

    # creates HTTP request DELETE ...
    response = requests.delete(url=send_calendar_url, headers=headers)
    if response.ok:
        return 'SUCCESS'
    else:
        return '{0}'.format(response.text)

