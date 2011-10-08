#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import os
from BasePageHandler import BaseHandler

class EntryHandler(BaseHandler):

	def get(self, slug):
		"""
		get the selected blog post details
		if not exist raise 404 page
		otherwise render entry detail page
		"""
		entry = self.db.get("SELECT * FROM entries WHERE slug= %s", slug)

		if not entry:
			raise tornado.web.HTTPError(404)
		
		self.render("entry.html", entry = entry)
