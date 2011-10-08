#!/usr/bin/evn python
import os.path
import re
import tornado.auth
import tornado.database
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata

from tornado.options import define, options

class BaseHandler(tornado.web.RequestHandler):

	"""
	this is base page handler 
	hold the reference for the db object so 
	that all the handler can access easily

	and also gives ability to get current user
	"""
	@property
	def db(self):
		return self.application.db

	def get_current_user(self):
		user_id = self.get_secure_cookie("user")

		if not user_id:
			return None
		return self.db.get("SELECT * FROM authors WHERE id = %s", int(user_id))