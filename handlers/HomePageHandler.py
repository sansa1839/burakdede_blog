#!/usr/bin/env python

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
from BasePageHandler import BaseHandler

class HomeHandler(BaseHandler):

 	def get(self):
 		"""
 		get the entries from db
 		if not entries redirect user to compose page
 		else show them all
 		"""
	 	entries = self.db.query("SELECT * FROM entries ORDER BY published DESC LIMIT 5")

	 	if not entries:
		 	self.redirect("/compose")
		 	return
		self.render("home.html", entries = entries)