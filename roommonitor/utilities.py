import json


# Amzazon Date: “today”: 2015-11-24
# Amazon Duration: “ten minutes”: PT10M, “five hours”: PT5H
# Amazon Time: “two fifteen pm”: 14:15
# MS DateTime: "2017-04-17T09:00:00",
# MS Duration : PT2H
def convert_amazon_to_ms(Date, Time):
    date_time = str(Date) + 'T' + str(Time)
    return date_time


def get_infor_from_alexa(Date, Time, Duration, Attendees):
    print(Date, Time, Duration,Attendees)
    vars['date'] = Date
    vars['time'] = Time
    vars['duration'] = Duration
    vars['attendees'] = Attendees


def store_locationConstraint(data):
    with open('locationConstraint.json', 'w') as json_file:
        json_file.write(json.dumps(data))


def load_locationConstraint():
    with open('locationConstraint.json') as json_file:
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
    data = load_locationConstraint()
    data['locations'].append(json_data)
    store_locationConstraint(data)