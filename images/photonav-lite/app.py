import tornado.web
import tornado.ioloop
from tornado import gen
import sys
import os
from stat import S_ISREG, ST_CTIME, ST_MODE
import sys
import time
import json


PHOTO_METADATA_FILE = 'photos.jsonl'
PHOTO_DIR = '/Volumes/Lilfoot/Pictures/phone_image_library/'
HTTP_PORT = 7777


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


if os.path.exists(PHOTO_METADATA_FILE):
    with open(PHOTO_METADATA_FILE, 'r') as infile:
        photos = [
            json.loads(line)
            for line in infile
        ]
else:
    photos = [
        {'path': photo, 'row': 0}
        for t, photo in get_date_sorted_files(
            PHOTO_DIR
        )
    ]


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


class PhotoCountHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        global photos
        self.write(json.dumps(len(photos)))


class IndexedPhotoHandler(BaseHandler):
    @gen.coroutine
    def get(self, i):
        global photos
        i = int(i)
        self.write(photos[i])
        # self.redirect('/img/{}'.format(photos[i]['path']))

    @gen.coroutine
    def put(self, i):
        global photos
        i = int(i)
        new_row = int(self.request.body)
        photos[i]['row'] = new_row


settings = {
    # 'cookie_secret': COOKIE_SECRET,
    # 'login_url': '/login',
    'debug': True
}

application = tornado.web.Application(
    [
        # (r'/', Handler),
        (r'/photos/count', PhotoCountHandler),
        (r'/imgnum/(.+?)', IndexedPhotoHandler),
        (
            r'/img/(.+?)',
            tornado.web.StaticFileHandler,
            {'path': PHOTO_DIR}
        )
    ],
    **settings
)

if __name__ == '__main__':
    print('Starting tornado server on port %d' % HTTP_PORT)
    application.listen(HTTP_PORT)
    ioloop = tornado.ioloop.IOLoop.instance()
    try:
        ioloop.start()
    except KeyboardInterrupt:
        print('KeyboardInterrupt, saving photos metadata...')
        with open(PHOTO_METADATA_FILE, 'w') as outfile:
            for photo in photos:
                outfile.write(json.dumps(photo) + '\n')
