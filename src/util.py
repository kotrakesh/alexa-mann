import re
import datetime
import json
import ms_endpoints
import room_class
import requests
import ssl
import urllib.request


tmp_locationConstraint_path = '/tmp/locationConstraint.json'            # not used
load_locationConstraint_path = './resources/locationConstraint.json'    # not used
url_locationConstraint      = 'https://sovanta.ddnss.de/writeToFile.php'            # script for uploading the file
url_locationConstraint_file = 'https://sovanta.ddnss.de/locationConstraint.json'    # path of remote database

room = room_class.Room()

################################################################################
# Functions


# Amzazon Date: “today”: 2015-11-24
# Amazon Duration: “ten minutes”: PT10M, “five hours”: PT5H
# Amazon Time: “two fifteen pm”: 14:15
# MS DateTime: "2017-04-17T09:00:00",
# MS Duration : PT2H
def convert_amazon_to_ms(Date, Time):
    date_time = str(Date) + 'T' + str(Time)
    return date_time

def create_event_from_alexa(start, end, title, room_name, cal_id):
    """Handler for create_event route."""
    print("cal id:"+cal_id)
    ms_endpoints.call_createvent(room.token, start, end, title, room_name, cal_id)

def timeSum(timeA, timeB):
    hoursA = re.search(r'(^[^:]+)', timeA).group(1)
    minutesA = re.search(r'([^:]+$)', timeA).group(1)
    hoursB = re.search(r'(^[^:]+)', timeB).group(1)
    minutesB = re.search(r'([^:]+$)', timeB).group(1)

    minutes = (int(minutesA) + int(minutesB))
    extraHour = int(minutes/60)
    minutes = minutes % 60
    hours = (extraHour + int(hoursA) + int(hoursB)) % 24

    if hours < 10:
        hours = "0" + str(hours)
    if minutes < 10:
        minutes = "0" + str(minutes)
    time = str(hours) + ":" + str(minutes)
    return time

def getMeetingEndTime(start, duration):
    if not re.search(r'\d\d:\d\d', start):
        start = start + ":00"
    if re.search(r'AF', start):
        if re.search(r'\b[1-9]\b', start):
            start = timeSum("0" + re.search(r'(\b[1-9]\b)', start).group(1) + ":00", "12:00")
        else:
            start = timeSum(re.search(r'(\d\d:\d\d)', start).group(1), "12:00")

    if re.search(r'\d*H', duration):
        hours = re.search(r'(\d*)H', duration).group(1)
    else:
        hours = '00'

    if re.search(r'\d*M', duration):
        minutes = re.search(r'(\d*)M', duration).group(1)
    else:
        minutes = '00'

    time = hours + ':' + minutes
    return timeSum(start, time)

### IO - Functions

def store_locationConstraint(data):
    '''
    Stores an updated version of the database on the server
    :param data: updated database content, will overwrite the current version on the server
    :return: return the http status code (200 for success)
    '''
    headers = {'content-type': 'application/json'}
    url = url_locationConstraint + '?text=' + str(data)
    r = requests.get(url, headers=headers, verify=False)
    return r.status_code


def load_locationConstraint():
    '''
    Loads the json database from the server
    :return: full content of the database
    '''
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(url_locationConstraint_file, context=ctx) as url:
        data = json.loads(url.read().decode())
        print(type(data))
        return data


def create_room_to_json(isAvailable, city, country, postalCode, state, street, displayName, email, attendees):
    '''
    Creates a new room in the json database, triggered from the Sovanta Dashboard "Raum erstellen"
    Loads the current version of the database and appends the new data for the new room and uploads it on the server
    :param isAvailable: shows the availability
    :param city:        city the room is located in
    :param country:     county the room is located in
    :param postalCode:  postal code of the city
    :param state:       state the room is located in
    :param street:      street the room is located in
    :param displayName: displayed Name of the calendar, this will be seen as a primary key to identify rooms, will be displayed in Outlook
    :param email:       email of the room
    :param attendees:   size of the room
    :return: http status code of uploading the file
    '''
    json_data = {
        "resolveAvailability": isAvailable,
        "address": {
            "city": city,
            "countryOrRegion": country,
            "postalCode": postalCode,
            "state": state,
            "street": street
        },
        "displayName": displayName,
        "locationEmailAddress": email,
        "maxAttendees": attendees
    }
    data = load_locationConstraint() #load from resources
    data['locations'].append(json_data)
    print('data appended')
    return store_locationConstraint(data)


def delete_room_to_json(name):
    '''
    Deletes a room from the database. Loads the current version and deletes the entry with the specific "display name"
    :param name: identifier of the room: display name
    :return: http status code of uploading the file
    '''
    print('delete room from json')
    data=load_locationConstraint()
    x=0
    for i in range(0, len(data['locations'])):
        if(data['locations'][i]['displayName']==name ):
            print("find it")
            x=i
        else:
            print("not find")

    data['locations'].pop(x)
    return store_locationConstraint(data)





#create_room_to_json('true', 'city', 'country', 'postalcode', 'state', 'street', 'display', 'email', 4)


### Old functions ###

# Solution for locally storing the database, only for development mode!!
def store_locationConstraint_local(data):
    with open('./resources/locationConstraint.json', 'w') as json_file:
        json_file.write(json.dumps(data))
        print(data)
def load_locationConstraint_local():
    with open('./resources/locationConstraint.json') as json_file:
        data = json.load(json_file)
        return data


# Tmp Solution for Storing database on lambda, not working !!
def store_locationConstraint_lambda(data):
    json_file = open(tmp_locationConstraint_path, 'w+')
    json_file.write(json.dumps(data))
    print(json_file)
    json_file.close()

    print('data to be added')
    print(json.dumps(data))
    try:
        new_file = open(tmp_locationConstraint_path, 'r')
        print('file has been opened in the /tmp directory')
        for l in new_file:
            print(str(l))
    except:
        print('file couldnt be found')

    try:
        #as lambda only allows writing access to the /tmp directory, this is a workaround
        shutil.copy2(tmp_locationConstraint_path, load_locationConstraint_path)
        print('store -- file was successfully copied to ./resources!')
    except:
        print('store -- copy of file failed')
def load_locationConstraint_lambda():
    data = ''
    try:
        with open(tmp_locationConstraint_path, 'r') as new_file:
            # print(new_file)
            print('file has been opened in the /tmp directory')
            # print(json.load(new_file))
            data = json.load(new_file)
            #return data
    except:
        # print('file couldnt be found, copy from ./resources')
        shutil.copy2(load_locationConstraint_path, tmp_locationConstraint_path)
        # print('load -- file was successfully copied to from ./resources to /tmp')
        data = json.load(open(load_locationConstraint_path, 'r'))
    finally:
        return data

