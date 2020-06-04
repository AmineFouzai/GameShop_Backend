
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
        self.write(tornado.escape.json_encode(dict(
            msg="unauthenticated client"
        )))


    def post(self):
        SessionID=uuid4()
        self.set_secure_cookie('SessionID',str(SessionID))
        user=tornado.escape.json_decode(self.request.body)
        client=model.User(email=user['email'],password=user['password'],SessionID=str(SessionID))
        if client.login(str(SessionID)): 
            user=client.find_user_by_SessionID(str(SessionID))
            # self.set_cookie('SessionID',str(SessionID))
            self.write(tornado.escape.json_encode(dict(
                SessionID=str(SessionID),
                encoded_jwt=jwt.encode(
                {   "id":str(user['_id']),
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
    
    @tornado.web.authenticated
    def get(self,_id):
        games=model.Game()
        if _id :
            self.write(tornado.escape.json_encode(games.find_one_by_id(_id)))
        else:
            self.write(tornado.escape.json_encode(games.get()))	
            
                
    @tornado.web.authenticated
    def post(self,arg):
        token=self.request.headers.get('Authorization').replace("Bearer ",'')
        user=jwt.decode(token,SECRET,algorithms=ALGORITHM)
        fileinfo=self.request.files['file'][0]
        filename=fileinfo["filename"]
        with open(UPLOADS+'/'+filename,'wb') as file:
            file.write(fileinfo['body'])
        games=model.Game(title=self.get_body_argument('title'),description=self.get_body_argument('description'),file_name=filename,user_id=user['id'])
        _id=games.add()
        self.write(tornado.escape.json_encode(dict(
            _id=str(_id.inserted_id),
            title=games.title,
            description=games.description,
            file_name=games.file_name
        )))

   

    @tornado.web.authenticated
    def delete(self,arg):
        token=self.request.headers.get('Authorization').replace("Bearer ",'')
        user=jwt.decode(token,SECRET,algorithms=ALGORITHM)
        game=tornado.escape.json_decode(self.request.body)
        games=model.Game(user_id=user['id'])
        game=games.delete(game['id'])
        os.remove(UPLOADS+'/'+game['file_name'])
        self.write(tornado.escape.json_encode(dict(
            _id=game['_id'],
            title=game['title'],
            description=game['description'],
            file_name=game['file_name']
        )))
        

    def options(self,arg):
        self.set_status(204)
        self.finish()



class DownloadGameRequestHandler(BaseHandler):
   
    @tornado.web.authenticated
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
                    self.write(tornado.escape.json_encode(dict(error="no file found ",code=404)))
            
