# The view handles requests and also does basic input validattion. It then passes the request into the controller. Wich further works with the request. 
class View:
    def __init__(self,app, cont):
        self.cont = cont		
        ## listen for the right things. 
        @app.route("/")
        def redir():
            return "<script>window.location.href =\"/static\"</script>"
        @app.route("/user/getkey/<username>/<password>")
        def authenticate(username, password):                           
            return self.cont.getapikey(username,password)
        @app.route("/user/add/<username>/<fullname>/<password>")
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
        @app.route("/notes/add/<content>/<apik>")
        def createnote(content, apik):
            if(" " in apik):
                return "supply valid apik"
            ## pass into controller and return the value that the controller returns. 
            return self.cont.addnote(content, apik)
        @app.route("/notes/arc/<noteid>/<apik>")
        def archivenote(noteid,apik):
            return self.cont.arcnote(noteid,apik)
        @app.route("/notes/del/<noteid>/<apik>")
        def deletenote(noteid,apik):
            return self.cont.delnote(noteid, apik)
        @app.route("/notes/ls/<apik>")
        def listnotes(apik):
            return self.cont.listnotes(apik)
        @app.route("/notes/lsarc/<apik>")
        def arcnotes(apik):
            return self.cont.listnotes(apik, 0)
        @app.route("/notes/unarc/<noteid>/<apik>")
        def unarc(noteid,apik):
            return self.cont.unarc(noteid,apik)
