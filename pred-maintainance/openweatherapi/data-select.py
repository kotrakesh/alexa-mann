
import json
import urllib2
import MySQLdb
import datetime


db = MySQLdb.connect(host="eu-cdbr-west-01.cleardb.com",
                     user="b3465148a734be",
                     passwd="a2c4eda1",
                     db="heroku_c0277ef6294fdf7")


cur = db.cursor()



cur.execute("SELECT * FROM current_data")

rows = cur.fetchall()

for row in rows:
    print(row)