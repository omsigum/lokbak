# The model all of the functions were data is manipulated. 
from conf import conf
import datetime
import json
import os
from binascii import hexlify
import mysql.connector
class Model:
    def adduser(self,username, fullname, password):
        cnx = self.createconnection()
        command = "call adduser('{}','{}','{}');".format(username, password, fullname);
        cursor = cnx.cursor()
        cursor.execute(command)
        cnx.commit()
        cursor.close()
        cnx.close()
        return True

    def addnote(content, userid):
        pass

    def createconnection(self):
        ## initalize a connection and return it 
        configobj = conf()
        config = {
                'user' : configobj.dbusername,
                'password' : configobj.dbpass,
                'host'     : configobj.dbhost,
                'database'  : configobj.dbase,
                'buffered': True
        }
        return mysql.connector.connect(**config) ## return the database object  
    def validtateapik(self, apik): 
        command = "select userID from apiKeys where aKey = '{}' and issued > date_sub(now(), interval 3 hour);".format(apik);
        cnx = self.createconnection()
        cursor = cnx.cursor()
        cursor.execute(command)
        result = cursor.fetchone()
        cnx.commit()
        cursor.close()
        cnx.close()
        if(result == None):
            return False
        else:
            return True
    def apikownsnote(self,apik,noteid):
        command = "select id from notes where userID = (select userID from apiKeys where aKey = '{}') and id = {}".format(apik,noteid)
        cnx = self.createconnection()
        cursor = cnx.cursor()
        cursor.execute(command)
        rv = cursor.fetchone()
        if(rv != None):
            return True
        return False

    def arcnote(self,noteid):
        command = "update notes set active = 0 where id = {}".format(noteid)
        cnx = self.createconnection()
        cursor = cnx.cursor()
        cursor.execute(command)
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    def listnotes(self,apik, ark = 1):
        command = "select id,content,added,lastEdited from notes where userID = (select userID from apiKeys where aKey = '{}') and active = {};".format(apik, ark)
        cnx = self.createconnection()
        cursor = cnx.cursor()
        cursor.execute(command)
        dicta = []
        rv = cursor.fetchone()
        while rv != None:
            bla = {}
            f = '%Y-%m-%d %H:%M:%S'
            bla['id'] = rv[0]
            bla['content'] = rv[1]
            bla['added']   = rv[2].strftime(f)
            bla['lastEdited'] = rv[3].strftime(f)
            dicta.append(bla)
            rv = cursor.fetchone()
        cursor.close()
        cnx.close()
        return json.dumps(dicta)
    def delnote(self,noteid):
        command = "delete from notes where id = {}".format(noteid)
        cnx = self.createconnection()
        cursor = cnx.cursor()
        cursor.execute(command)
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    def addnote(self,content,apik):
        command = "insert into notes(userID, content) VALUES ((select userID from apiKeys where aKey = '{}'), '{}');".format(apik, content);          
        cnx = self.createconnection()
        cursor = cnx.cursor()
        cursor.execute(command)
        cnx.commit()
        cursor.close()
        cnx.close()
        return True

    def getapikey(self,username):
        cnx = self.createconnection()
        command = "select getapikey({});".format(self.getuserid(username));
        cursor = cnx.cursor()
        cursor.execute(command)
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        if(result[0] == None):
            if self.genapikey(username):
                return self.getapikey(username)
            else:
                return "failure"
        return result
    
    def genapikey(self,username):
        key = hexlify(os.urandom(255))
        command = "call addapikey('{}','{}');".format(self.getuserid(username), key.decode())
        cnx = self.createconnection()
        cursor = cnx.cursor()
        cursor.execute(command)
        cnx.commit()
        cursor.close()
        cnx.close()
        return True

    def getuserid(self, username):
        cnx  = self.createconnection()
        cursor = cnx.cursor()
        command = ("select id from users where username = '{}';".format(username));
        cursor.execute(command)
        rv = cursor.fetchone()
        cnx.commit()
        cursor.close()
        cnx.close()
        return str(rv[0])

    def getpass(self,username):
        cnx = self.createconnection()
        cursor = cnx.cursor()
        command = "select hash from users where username = '{}';".format(username)
        cursor.execute(command)
        rv = cursor.fetchone()
        cnx.commit()
        cnx.close()
        cursor.close()
        return str(rv[0])

