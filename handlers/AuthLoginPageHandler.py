#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import os

from BasePageHandler import BaseHandler

class AuthLoginHandler(BaseHandler, tornado.auth.GoogleMixin):

	@tornado.web.asynchronous
	def get(self):
		"""
		call to open id google account
		module to authenticate user
		"""
		if self.get_argument("openid.mode", None):
			self.get_authenticated_user(self.async_callback(self._on_auth))
			return
		self.authenticate_redirect()

	def _on_auth(self,user):
		"""
		if user do not match on users table 
		do not authenticate user via google account
		raise http 500 error

		else save the first user authenticated as
		administrator and set the cookie if already one entry
		exist in user table
		"""
		if not user:
			raise tornado.web.HTTPError(500, "Google auth failed")
		author = self.db.get("SELECT * FROM authors WHERE email = %s", user["email"])

		if not author:
			any_author = self.db.get("SELECT * FROM authors LIMIT 1")
			if not any_author:
				author_id = self.db.execute(
					"INSERT INTO authors (email,name) VALUES(%s,%s)",
					user["email"],user["name"])
			else:
				self.redirect("/")
				return
		else:
			author_id = author["id"]
			self.set_secure_cookie("user", str(author_id))
			self.redirect(self.get_argument("next", "/"))
