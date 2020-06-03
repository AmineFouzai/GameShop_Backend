
'''
Middleware for controller to contain all the modules
'''
import tornado.web
import tornado.escape
import jwt
import json
from uuid import uuid4
from models import model
import os