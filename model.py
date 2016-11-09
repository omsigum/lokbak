from conf import conf
import mysql.connector
class Model:
	def __init__(self):
		print("model in") 
	def adduser(self,username, fullname, password):
		cnx = self.createconnection()
		## make the query
		command = ("call adduser('{}','{}','{}');".format(username, password, fullname));
		args = (username, password, fullname)	
		cursor = cnx.cursor()
		result = cursor.callproc('adduser',args)
		print(result[0] + "outcome")
	#	for result in cursor.execute(command, multi=True):
	#		print("hey")
		cursor.close()
		cnx.close()
		return True
	def hashpassword(password):
		pass
		return hashedpass
	def printhey(self):
		print("hey")
	def addnote(content, userid):
		pass
	def addapikey(self):
		print("print")
	def createconnection(self):
		## initalize a connection and return it 
		configobj = conf()
		config = {
			'user' : configobj.dbusername,
			'password' : configobj.dbpass,
			'host'     : configobj.dbhost,
			'database'  : configobj.dbase
		}
		return mysql.connector.connect(**config) ## return the database object  
						




# cnx = creconnection()
#  9     cursor = cnx.cursor()
#  8     query = ("select npassinflight('"+numb+"','"+date+"');");
#  7     cursor.execute(query);
#  6     output = ""
#  5     for (x) in cursor:
#  4         temp = str(x)[1:]
#  3         temp = temp[:-2]
#  2         return temp
#  1     cursor.close()
#  0     cnx.close()

