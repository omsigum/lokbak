from passlib.hash import pbkdf2_sha256 as passs
# the function of the controller. Stand between the model and the view in order to easily make future modifications to functionality. This happens without the view or the model being changed and happens in the samt place 
class Con:
	def __init__(self,modl):
		self.modl = modl
		# make the model initalize a connection 
	def adduser(self,username, fullname, password):
		## hash the password and then move the information into the model. 
		password = self.hashpasscode(password)	
		return self.modl.adduser(username,fullname,password)
	def hashpasscode(self, password):
		return passs.encrypt(password,rounds=20000, salt_size=16)		
