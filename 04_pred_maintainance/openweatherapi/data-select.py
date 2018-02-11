import pymysql

from classCommonF import classCommonF

classCommonF = classCommonF()

cnx = classCommonF.dataBaseConnection()
cur = cnx.cursor()

cur.execute("SELECT * FROM current_data")# selecting all the data form current_data table

rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()