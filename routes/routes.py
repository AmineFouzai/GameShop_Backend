from tornado.web import url
from controllers import *
route = [
url(r'/signup',handlers.SignupRequestHandler),
url(r'/login',handlers.LoginRequestHandler),
url(r'/logout',handlers.LogoutRequestHandler),
url(r'/games',handlers.GameCRUDRequestHandler),
url(r'/game/download'+r'/(.*)',handlers.DownloadGameRequestHandler),
url(r'/user',handlers.UserRequestHnadler)
]
