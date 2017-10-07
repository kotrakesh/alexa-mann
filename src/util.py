import re
import json
import ms_endpoints
import room_class
import requests
import ssl
import urllib.request
import pprint


tmp_locationConstraint_path = '/tmp/locationConstraint.json'            # not used
load_locationConstraint_path = './resources/locationConstraint.json'    # not used
url_locationConstraint      = 'https://sovanta.ddnss.de/writeToFile.php'            # script for uploading the file
url_locationConstraint_file = 'https://sovanta.ddnss.de/locationConstraint.json'    # path of remote database

room = room_class.Room()
pp = pprint.PrettyPrinter(indent=4)

################################################################################

### Time functions ###
def convert_amazon_to_ms(Date, Time):
    '''
    Converts the time format from Amazon to MS format
    :param Date: date
    :param Time: time
    :return: concatenation of date and time
    '''
    date_time = str(Date) + 'T' + str(Time)
    return date_time

def timeSum(timeA, timeB):
    '''
    Sums two times in HH:MM 24h format together.
    :param timeA: Time in the HH:MM 24h format as string
    :param timeB: Time in the HH:MM 24h format as string which you want to add to timeA
    :return: Sum of timeA and timeB. Time sums over 23:59 starts from 00:00 again. 
    '''
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
    '''
    Takes a start time in HH:MM 24h format, adds the Amazon duration to it
    and returns the end time in HH:MM 24h format.
    :param start: Starting time in the HH:MM 24h format as string
    :param duration: Amazon duration format
    :return: Meeting end time in the HH:MM 24h format as string
    '''
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


### IO - Functions ###

def store_locationConstraint(data):
    '''
    Stores an updated version of the database on the server
    :param data: updated database content, will overwrite the current version on the server
    :return: return the http status code (200 for success)
    '''
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url_locationConstraint, data=json.dumps(data), headers=headers, verify=False)
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
        #pp.pprint(data)
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
    # new added data
    data = load_locationConstraint()
    data['locations'].append(json_data)
    print('data appended')
    return store_locationConstraint(data)


def delete_room_to_json(name):
    '''
    Deletes a room from the database. Loads the current version and deletes the entry with the specific "display name"
    :param name: identifier of the room: display name
    :return: http status code of uploading the file
    '''
    data=load_locationConstraint()
    x=0
    for i in range(0, len(data['locations'])):
        if(data['locations'][i]['displayName'] == name):
            print("find room")
            x=i
        else:
            print("couldnt find room")

    data['locations'].pop(x)
    return store_locationConstraint(data)


# Testing
#load_locationConstraint()
#create_room_to_json("true", "city", "country", "postalcode", "state", "street", "display", "email", 4)



### Old functions ###

# Solution for locally storing the database, only for DEVELOPMENT mode!!
def store_locationConstraint_local(data):
    with open('./resources/locationConstraint.json', 'w') as json_file:
        json_file.write(json.dumps(data))

def load_locationConstraint_local():
    with open('./resources/locationConstraint.json') as json_file:
        data = json.load(json_file)
        return data


# Tmp Solution for Storing database on LAMBDA, not working !!
def store_locationConstraint_lambda(data):
    json_file = open(tmp_locationConstraint_path, 'w+')
    json_file.write(json.dumps(data))
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

