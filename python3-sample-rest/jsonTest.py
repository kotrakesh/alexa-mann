import json
import time

def store(data):
    with open('test.json', 'w') as json_file:
        json_file.write(json.dumps(data))


def load():
    with open('test.json') as json_file:
        data = json.load(json_file)
        return data

if __name__ == "__main__":
    newData ={

      "address": {
        "city": "Heidelberg",
        "countryOrRegion": "Deutschland",
        "postalCode": "69115",
        "state": "Baden-Wuerttemberg",
        "street": "Mittermaierstraße 31"
      },
      "displayName": "Meetingroom new",
      "locationEmailAddress": "meetingroom1@sovanta.de",
      "maxAttendees": 50
    }

    data = load()
    data['locations'].append(newData)
    store(data)
    for l in data['locations']:
        print(l)
