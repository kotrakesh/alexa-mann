import re
import datetime

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

print(getMeetingEndTime("14:00", "PT3H12M"))
#print(getMeetingEndTime("10:20","PT12H10M50S"))

