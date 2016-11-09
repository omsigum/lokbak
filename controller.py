# the function of the controller. Stand between the model and the view in order to easily make future modifications to functionality. The controller has acces to the models functions. The model is like a work horse and can validate and take action while the controller uses the information from the model to make decisions about what to do.  
from passlib.hash import pbkdf2_sha256 as passs
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
    def authuser(self, username, password):
        passhash = self.modl.getpass(username)
        if( passs.verify(password, passhash) ):
            ## user verified. 
            return True
        return False
    def getapikey(self, username,password):
        if(self.authuser(username,password)):
            return self.modl.getapikey(username) 
    def addnote(self,content, apik):
        ## validate the apik.
        if(self.modl.validtateapik(apik)):
            # The key is valid. continue and add the note. 
            if(self.modl.addnote(content,apik)):
                return "note has been created"
        else:
            return "key is not valid"
    def listnotes(self,apik, ark = 1):
        if(self.modl.validtateapik(apik)):
                return self.modl.listnotes(apik, ark)
        else:
            return "key is not valid"
    def arcnote(self, noteid, apik):
        if(self.modl.apikownsnote(apik, noteid)):
            ## the apik owns the noteid. continue with update. 
            if(self.modl.arcnote(noteid)):
                return "active status has been updated"
            else:
                return "something went wrong" 
        else:
            return "you are either not owner of fhe noteid and/or apik does not exists."
            
    def delnote(self,noteid,apik):
        if(self.modl.apikownsnote(apik,noteid)):
            ## del the note
            if(self.modl.delnote(noteid)):
                return "note has been deleted"
            else:
                return "something went wrong"
        else:
            return "you are either not owner of fhe noteid and/or apik does not exists."
