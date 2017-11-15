import conf
import pymysql

class classCommonF:
	def dataBaseConnection(self):# data base connection objects
		cnx = pymysql.connect(user=conf.dbUser, password=conf.dbPassowrd,
                                  host=conf.dbHost,
                                  database=conf.dbDatabase)
		cursor = cnx.cursor()
		return cnx
