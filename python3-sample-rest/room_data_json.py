import json

def addMeetingRoomToDB(isAvailable, city, country, postalCode, state, street, displayName, email, attendees):
    json_data = json.dumps({
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
      "maxAttendees" : attendees
    })
    return json_data

#print(addMeetingRoomToDB(True, "Heidelberg", "Germany", "69115", "Baden-Wuerttemberg",
#                        "Mittermaierstraße 31", "Meetingroom X", "xyz@sovanta.de", 6))

