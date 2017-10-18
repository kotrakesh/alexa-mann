import config
import pymysql

class classCommonFunc:
	def dataBaseConnection(self):
		#creating data base connection woth data base parameters
		cnx = pymysql.connect(user=config.dbUser, password=config.dbPassowrd,
                                  host=config.dbHost,
                                  database=config.dbDatabase)
		cursor = cnx.cursor()
		# print("Database connection set up")
		return cnx