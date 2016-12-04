import tornado.web
import tornado.ioloop


port = 7777

photo_dir = 'sample_photos'

class Handler(tornado.web.RequestHandler):
    def get(self):
        self.write('hello_world')

settings = {
    # "cookie_secret": COOKIE_SECRET,
    # "login_url": "/login",
    "debug": True
}


application = tornado.web.Application(
    [
        (r"/", Handler),
    ],
    **settings
)


if __name__ == "__main__":
    application.listen(port)
    print "starting tornado server on port %s" % port
    tornado.ioloop.IOLoop().instance().start()
