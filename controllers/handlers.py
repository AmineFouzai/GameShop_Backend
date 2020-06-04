
'''
Preset controller by torn for / route
'''
from .modules import *

UPLOADS=os.environ.get('UPATH')
SECRET=os.environ.get('SECRET')
ALGORITHM=os.environ.get('ALGORITHM')
class BaseHandler(tornado.web.RequestHandler):
        
    def get_current_user(self):
        return self.get_secure_cookie('SessionID')


class UserRequestHnadler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("access-control-allow-origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')
        self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type") 
    
    def put(self):
        token=self.request.headers.get('Authorization').replace("Bearer ",'')
        user=jwt.decode(token,SECRET,algorithms=ALGORITHM)
        user_record=tornado.escape.json_decode(self.request.body)
        client=model.User(name=user_record['name'],email=user_record['email'],password=user_record['password'])
        new_user_record=client.update(user['id'])
        self.write(tornado.escape.json_encode(dict(
            SessionID=new_user_record['SessionID'],
            encoded_jwt=jwt.encode(
            {
                "id":str(user['id']),
                "name":new_user_record['name'],
                "email":new_user_record['email'],
                "password":new_user_record['password']
            },SECRET, algorithm=ALGORITHM).decode('UTF-8')
            )))
    
    def delete(self):
        token=self.request.headers.get('Authorization').replace("Bearer ",'')
        user=jwt.decode(token,SECRET,algorithms=ALGORITHM)
        client=model.User()
        self.write(tornado.escape.json_encode(client.delete(user['id'])))
 
    def options(self):
        self.set_status(204)
        self.finish()
    

class SignupRequestHandler(BaseHandler):
    
    def set_default_headers(self):
        self.set_header("access-control-allow-origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')
        self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type") 

    def post(self):   
        SessionID=uuid4()
        self.set_secure_cookie('SessionID',str(SessionID))
        user=tornado.escape.json_decode(self.request.body)
        client=model.User(name=user['name'],email=user['email'],password=user['password'],SessionID=str(SessionID))
        if not client.add_user():
            self.set_status(status_code=403)
            self.write(tornado.escape.json_encode(dict(msg='user already exist')))
        else:
            client.add_user()
            user=client.find_user_by_SessionID(str(SessionID))
            self.write(tornado.escape.json_encode(dict(
                SessionID=str(SessionID),
                encoded_jwt=jwt.encode(
                {   "id":str(user['_id']),
                    "name":user['name'],
                    "email":user['email'],
                    "password":user['password']
                },SECRET, algorithm=ALGORITHM).decode('UTF-8')
                )))
    
    def options(self):
        self.set_status(204)
        self.finish()
        

class LoginRequestHandler(BaseHandler):
    
    def set_default_headers(self):
        self.set_header("access-control-allow-origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')
        self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type") 

    def get(self):
        self.set_status(status_code=401)
        self.write(tornado.escape.json_encode(dict(msg="unauthenticated client")))

    def post(self):
        SessionID=uuid4()
        self.set_secure_cookie('SessionID',str(SessionID))
        user=tornado.escape.json_decode(self.request.body)
        client=model.User(email=user['email'],password=user['password'],SessionID=str(SessionID))
        if client.login(str(SessionID)): 
            user=client.find_user_by_SessionID(str(SessionID))
            self.write(tornado.escape.json_encode(dict(
                SessionID=str(SessionID),
                encoded_jwt=jwt.encode(
                {
                    "id":str(user['_id']),
                    "name":user['name'],
                    "email":user['email'],
                    "password":user['password']
                },SECRET, algorithm=ALGORITHM).decode('UTF-8')
                )))
        
        else:
            self.set_status(status_code=404)
            self.write(tornado.escape.json_encode(dict(msg='user does not exist')))
    
    def options(self):
        self.set_status(204)
        self.finish()


class LogoutRequestHandler(BaseHandler):
       
    def set_default_headers(self):
        self.set_header("access-control-allow-origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')
        self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type") 
    
    def get(self):
            self.clear_all_cookies()
            self.redirect('/login')

    def options(self,arg):
        self.set_status(204)
        self.finish()



class GameCRUDRequestHandler(BaseHandler):

    def set_default_headers(self):
        self.set_header("access-control-allow-origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')
        self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type") 
    
    def get(self):
        games=model.Game()
        self.write(tornado.escape.json_encode(games.get()))	
            
    def post(self):        
        token=self.request.headers.get('Authorization').replace("Bearer ",'')
        user=jwt.decode(token,SECRET,algorithms=ALGORITHM)
        fileinfo=self.request.files['file'][0]
        filename=fileinfo["filename"]
        with open(UPLOADS+'/'+filename,'wb') as file:
            file.write(fileinfo['body'])
        games=model.Game(title=self.get_body_argument('title'),description=self.get_body_argument('description'),file_name=filename,user_id=user['id'],user_name=user['name'])
        _id=games.add()
        self.write(tornado.escape.json_encode(dict(
            _id=str(_id.inserted_id),
            name=user['name'],
            title=games.title,
            description=games.description,
            file_name=games.file_name
        )))

    def delete(self):
        token=self.request.headers.get('Authorization').replace("Bearer ",'')
        user=jwt.decode(token,SECRET,algorithms=ALGORITHM)
        game=tornado.escape.json_decode(self.request.body)
        games=model.Game(user_id=user['id'],user_name=user['name'])
        game=games.delete(game['id'])
        os.remove(UPLOADS+'/'+game['file_name'])
        self.write(tornado.escape.json_encode(dict(
            _id=game['_id'],
            title=game['title'],
            description=game['description'],
            file_name=game['file_name']
            )))
        
    def options(self):
        self.set_status(204)
        self.finish()



class DownloadGameRequestHandler(BaseHandler):
   
    def get(self,filename):
            if filename:
                buf_size=4069
                self.set_header('Content-Type','appliacation/octet-stream')
                self.set_header('Content-Disposition','attachment;filename={}'.format(filename))
                with open(UPLOADS+'/'+filename,'rb') as file:
                    while True:
                        data=file.read(buf_size)
                        if not data :
                            break
                        self.write(data)                
            else:
                self.set_status(status_code=404)
                self.write(tornado.escape.json_encode(dict(msg="no file found ")))
            
