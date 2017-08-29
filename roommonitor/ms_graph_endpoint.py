import json
import requests
import uuid

#from flask import Flask, redirect, url_for, session, request, render_template



# Events
def call_createvent_endpoint(access_token,tStart,tEnd,title,roomName, cal_id):
    """Call the resource URL for the create event action."""
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

    # Create the email that is to be sent via the Graph API
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


def call_listevents_for_time_endpoint(access_token, id, start, end):
    list_events_url = 'https://graph.microsoft.com/v1.0/me/calendars/' + id + '/calendarView?startDateTime=' + start + 'Z&endDateTime=' + end + 'Z'
    # set request headers
    #print(list_events_url)
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


# Calendars
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


def call_deletecalendar_endpoint(access_token, id):
    """Call the resource URL for the sendMail action."""
    send_calendar_url = 'https://graph.microsoft.com/v1.0/me/calendars/'+id

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
    response = requests.delete(url=send_calendar_url, headers=headers)
    if response.ok:
        return 'SUCCESS'
    else:
        return '{0}'.format(response.text)
