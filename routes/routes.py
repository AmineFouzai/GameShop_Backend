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
				
