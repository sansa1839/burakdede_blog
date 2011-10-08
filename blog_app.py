#!/usr/bin/env python

"""
This is the main application class for my blog
hosting application object, handler patterns
and other stuff like settings
"""
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
from handlers.HomePageHandler import HomeHandler
from handlers.EntryPageHandler import EntryHandler
from handlers.AuthLoginPageHandler import AuthLoginHandler
from handlers.AuthLogoutPageHandler import AuthLogoutHandler
from handlers.ComposePageHandler import ComposeHandler
from handlers.EntryUIModule import EntryModule

define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="blog", help="blog database name")
define("mysql_user", default="root", help="blog database user")
define("mysql_password", default="", help="blog database password")

class Application(tornado.web.Application):
	
	def __init__(self):
		"""
		initializer for application object
		"""		

		handlers = [
			(r"/", HomeHandler),
			(r"/entry/([^/]+)", EntryHandler),
			(r"/auth/login", AuthLoginHandler),
			(r"/auth/logout", AuthLogoutHandler),
			(r"/compose", ComposeHandler),
		]

		settings = dict(
			blog_title = "Notes From Self Development Freak",
			template_path = os.path.join(os.path.dirname(__file__), "templates"),
			static_path = os.path.join(os.path.dirname(__file__),"static"),
			ui_modules={"Entry": EntryModule},
			cookie_secret = "11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
			xsrf_cookies = True,
			login_url = "/auth/login",
			autoescape = None,
			debug=True,
		)

		tornado.web.Application.__init__(self,handlers,**settings)
		self.db = tornado.database.Connection(
			host = options.mysql_host, database=options.mysql_database,
			user = options.mysql_user, password=options.mysql_password)

def main():
	"""
	no magic its just parse the command line options
	start server with appilcation object
	listen to given port from options
	and start ioloop
	"""
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
	main()
