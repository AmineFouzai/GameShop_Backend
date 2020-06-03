from tornado.web import url
from controllers import *
route = [
		url(
			r'/games',
			handlers.GameCRUDRequestHandler
		),
		url(
			r'/games'+r'/(.*)',
			handlers.GameCRUDRequestHandler
		),
		url(
			r'/signup',
			handlers.SignupRequestHandler
		),
		url(
			r'/login',
			handlers.LoginRequestHandler
		),
		url(
			r'/logout',
			handlers.LogoutRequestHandler	
		),
		url(
			r'/game/download'+r'/(.*)',
			handlers.DownloadGameRequestHandler
		)


]
				
'''
/home
/settings
/login
/signup


GET /games
POST /games
PUT /games
DELETE /games
GET /clients
POST /clients
PUT /clients
DELETE /clients
GET /games/:id
GET /clients/:id
'''