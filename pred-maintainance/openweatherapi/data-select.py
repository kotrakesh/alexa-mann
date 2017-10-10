import pymysql

from classCommonF import classCommonF

classCommonF = classCommonF()

cnx = classCommonF.dataBaseConnection()
cur = cnx.cursor()

cur.execute("SELECT * FROM current_data")

rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()