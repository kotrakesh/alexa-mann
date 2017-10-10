import pymysql

from classCommonFunc import classCommonFunc

classCommonFunc = classCommonFunc()

cnx = classCommonFunc.dataBaseConnection()
cur = cnx.cursor()

cur.execute("SELECT * FROM current_data")

rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()