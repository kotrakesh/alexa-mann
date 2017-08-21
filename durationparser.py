
import datetime

start = '10:10'
duration = '5:80'

timeList = [start, duration]
sum = datetime.timedelta()
for i in timeList:
    (h, m) = i.split(':')
    d = datetime.timedelta(hours=int(h), minutes=int(m))
    sum += d
print(str(sum))
