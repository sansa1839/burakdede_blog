#!/usr/bin/env python

import tornado.web
import tornado.ioloop
import os

from BasePageHandler import BaseHandler

class AuthLogoutHandler(BaseHandler):

	"""
	just simple clear the cookie of 
	the user and set user back to the root of app
	"""
	def get(self):
		self.clear_cookie("user")
		self.redirect(self.get_argument("next","/"))