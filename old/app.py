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
        self.render(
            'templates/home.html',
            images=list(datastore['images'].find())
        )


class UpdateHandler(tornado.web.RequestHandler):
    def get(self):
        for image_path in glob.glob(photo_dir + '*.jpg'):
            print(image_path)
            md5 = hasher.md5(image_path)
            if datastore['images'].find_one(md5=md5) is None:
                print('new photo')
                datastore['images'].insert({
                    'md5': md5,
                    'path': image_path,
                    'v_index': 0,
                    'h_index': 0
                })
            else:
                print(datastore['images'].find_one(md5=md5))


class ImageHandler(tornado.web.RequestHandler):
    def get(self, h_index, v_index):
        results = datastore.query(
            '''
            SELECT * FROM images
            WHERE h_index={h_index}
            AND v_index={v_index};
            '''.format(
                h_index=h_index,
                v_index=v_index
            )
        )
        image = next(results)

        # image = datastore['images'].find_one(
        #     id=str(
        #         (
        #             int(img_id) % len(list(
        #                 datastore['images'].find()
        #             ))
        #         ) + 1
        #     )
        # )
        with open(image['path'], 'rb') as infile:
            self.finish(infile.read())


settings = {
    # 'cookie_secret': COOKIE_SECRET,
    # 'login_url': '/login',
    'debug': True
}

application = tornado.web.Application(
    [
        (r'/', Handler),
        (r'/update', UpdateHandler),
        (r'/images/(.+?)\.(.+?)', ImageHandler),
        (r'/css/(.+)', tornado.web.StaticFileHandler, {'path': './static/css/'}),
        (r'/js/(.+)', tornado.web.StaticFileHandler, {'path': './static/js/'})
    ],
    **settings
)


if __name__ == '__main__':
    application.listen(port)
    print('starting tornado server on port %s' % port)
    tornado.ioloop.IOLoop().instance().start()
