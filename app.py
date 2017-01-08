import tornado.web
import tornado.ioloop
import dataset
import glob
from tools import hasher
import os


port = 7777

photo_dir = './sample_photos/'

mypath = os.path.dirname(os.path.realpath(__file__))

PERSISTENT_PATH = mypath
DATASTORE_PATH = 'sqlite:///%s/datastore.db' % PERSISTENT_PATH
datastore = dataset.connect(DATASTORE_PATH)


class Handler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/home.html')

class UpdateHandler(tornado.web.RequestHandler):
    def get(self):
        for image_path in glob.glob(photo_dir + '*.jpg'):
            md5 = hasher.md5(image_path)
            if datastore['images'].find_one(md5=md5) is None:
                datastore['images'].insert({
                    'md5': md5,
                    'row': 0
                })


settings = {
    # "cookie_secret": COOKIE_SECRET,
    # "login_url": "/login",
    "debug": True
}

application = tornado.web.Application(
    [
        (r"/", Handler),
        (r"/update", UpdateHandler)
    ],
    **settings
)



if __name__ == "__main__":
    application.listen(port)
    print("starting tornado server on port %s" % port)
    tornado.ioloop.IOLoop().instance().start()
