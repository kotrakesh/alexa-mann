import re
import datetime

start = '10:10'
duration = 'PT12H5M50S'

if bool(re.search(r'\d*H', duration)):
    hours = re.search(r'(\d*)H', duration).group(1)
else:
    hours = '00'

if bool(re.search(r'\d*M', duration)):
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

print('The meeting ends at: ' + str(sum))
