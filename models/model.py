from pymongo import MongoClient
from pymongo import ReturnDocument
from  tornado.escape import json_decode
from bson.json_util import dumps
from bson import decode_all,ObjectId
import hashlib

CLIENT=MongoClient(os.environ.get('URI'))
        
class User(object):
    def __init__(self,name=None,email=None,password=None,SessionID=None):
        self.db=CLIENT.users
        self.name=name
        self.email=email
        self.password=hashlib.sha256(str(password).encode('UTF-8')).hexdigest()
        self.SessionID=SessionID
        
    def add_user(self):
    
        return self.db.user.insert_one({
            "name":self.name,
            "email":self.email,
            "password":self.password,
            'SessionID':self.SessionID
        }) if not self.authanticate(email=self.email,password=self.password) else False
        
    def find_user_by_SessionID(self,SessionID):
        document=self.db.user.find_one({'SessionID':SessionID})
        return document


    def authanticate(self,email,password):
        user=dict()
        document=self.db.user.find_one({'email':email,'password':password})
        return True if document else False

    def login(self,SessionID):
        if self.authanticate(email=self.email,password=self.password):
            self.db.user.find_one_and_update({'email':self.email,'password':self.password},{"$set":{"SessionID":str(SessionID)}})
            return True
        else:
            return False





class Game(object):

    def __init__(self,title=None,description=None,file_name=None,user_id=None):
        self.db=CLIENT.games
        self.title=title
        self.description=description
        self.file_name=file_name
        self.user_id=user_id

    def add(self):
        
        return self.db.game.insert_one({
            "title":self.title,
            "description":self.description,
            "file_name":self.file_name,
            "user_id":self.user_id
            })
        
    def delete(self,_id):
        document=self.db.game.find_one_and_delete({"_id":ObjectId(_id)})
        document['_id']=str(document['_id'])
        return document

    def update(self,_id):

        document= self.db.game.find_one_and_update(
            {
                "_id":ObjectId(_id)
            },{
                "$set":{
                    "title":self.title,
                    "description":self.description,
            }
            },return_document=ReturnDocument.AFTER)
        document['_id']=str(document['_id'])
        return document
        
    def find_one_by_id(self,_id):
        document= self.db.game.find_one({"_id": ObjectId(_id)})
        document['_id']=str(document['_id'])
        return document

    def get(self):
        data=list()
        documents=self.db.game.find({})
        for document in documents:
            document['_id']=str(document['_id'])
            print(document)
            data.append(document)
        return data
    
       



