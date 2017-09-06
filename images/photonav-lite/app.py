import tornado.web
import tornado.ioloop
from tornado import gen
import sys
import os
from stat import S_ISREG, ST_CTIME, ST_MODE
import sys
import time


port = 7777

def get_date_sorted_files(dirpath):
    # get all entries in the directory w/ stats
    entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
    entries = ((os.stat(path), path) for path in entries)

    # leave only regular files, insert creation date
    entries = ((stat[ST_CTIME], path)
               for stat, path in entries if S_ISREG(stat[ST_MODE]))
    #NOTE: on Windows `ST_CTIME` is a creation date 
    #  but on Unix it could be something else
    #NOTE: use `ST_MTIME` to sort by a modification date

    for cdate, path in sorted(entries):
        yield time.ctime(cdate), os.path.basename(path)


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header(
            'Access-Control-Allow-Headers',
            'authorization, Authorization, Content-Type, '
            'Depth, User-Agent, X-File-Size, X-Requested-With, '
            'X-Requested-By, If-Modified-Since, X-File-Name, Cache-Control'
        )
        self.set_header('Access-Control-Allow-Methods', 'PUT, DELETE, POST, GET, OPTIONS')

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()


class Handler(BaseHandler):
    @gen.coroutine
    def get(self):
        self.write({
            'photos': [
                image
                for t, image in get_date_sorted_files(
                    '/Volumes/Lilfoot/Pictures/phone_image_library/'
                )
            ][:100]
        })


settings = {
    # 'cookie_secret': COOKIE_SECRET,
    # 'login_url': '/login',
    'debug': True
}


application = tornado.web.Application(
    [
        (r'/', Handler),
        (
            r'/img/(.+?)',
            tornado.web.StaticFileHandler,
            {'path': '/Volumes/Lilfoot/Pictures/phone_image_library/'}
        )
    ],
    **settings
)

HTTP_PORT = 7777

if __name__ == '__main__':
    print('Starting tornado server on port %d' % HTTP_PORT)
    application.listen(HTTP_PORT)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()
