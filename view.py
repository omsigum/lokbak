class View:
	def __init__(self,app, cont):
		self.cont = cont		
		## listen for the right things. 
		print("view initalized")
		@app.route("/getapikey/<username>/<password>")
		def authenticate(username, password):
			return username + " " + password


		@app.route("/createuser/<username>/<fullname>/<password>")
		def createuser(username = None, fullname = None, password = None):
			## validate the input  
			if(username == None or fullname == None or password == None):
				return "{\"Please provide a valid input\"}"
			if(" " in username or " " in password):
				return "{\"Please provide a valid input\"}"
			## input is valid move on 	
			if self.cont.adduser(username,fullname,password):
				return "user has been added"
			else:
				return "something went wrong. user was not added"
					
