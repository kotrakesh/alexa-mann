import re
import datetime
import json
import ms_endpoints
import room_class
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


def getMeetingEndTime(start, duration):

    if re.search(r'\d*H', duration):
        hours = re.search(r'(\d*)H', duration).group(1)
    else:
        hours = '00'

    if re.search(r'\d*M', duration):
        minutes = re.search(r'(\d*)M', duration).group(1)
    else:
        minutes = '00'

    time = hours + ':' + minutes

    timeList = [start, time]
    sum = datetime.timedelta()
    for i in timeList:
        (h, m) = i.split(':')
        d = datetime.timedelta(hours=int(h), minutes=int(m))
        sum += d

    if len(str(sum)) < 8:
        return  '0' + str(sum)
    return str(sum)

# Check the right filepath
def store(data):
    with open('./resources/locationConstraint.json', 'w') as json_file:
        json_file.write(json.dumps(data))


def load():
    with open('./resources/locationConstraint.json') as json_file:
        data = json.load(json_file)
        return data


def create_room_to_json(isAvailable, city, country, postalCode, state, street, displayName, email, attendees):
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
    data = load()
    data['locations'].append(json_data)
    store(data)

load()