import config
import pymysql

class classCommonFunc:
	def dataBaseConnection(self):
		cnx = pymysql.connect(user=config.dbUser, password=config.dbPassowrd,
                                  host=config.dbHost,
                                  database=config.dbDatabase)
		x = cnx.cursor()
		return cnx
