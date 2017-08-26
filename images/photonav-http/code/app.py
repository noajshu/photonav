import tornado.web
import tornado.ioloop
from tornado.web import authenticated
from tornado import gen
from tools import crypto
import os
from tools.sessions import Sessionable


port = 7777

mypath = os.path.dirname(os.path.realpath(__file__))


# create cookie_secret if it doesn't exist
if not os.path.exists(mypath + '/cookie_secret'):
    with open(mypath + '/cookie_secret', 'wb') as outfile:
        outfile.write(str(crypto.random_integer(10**4)).encode())

with open(mypath + '/cookie_secret', 'rb') as infile:
    COOKIE_SECRET = infile.read()


# priority override goes to first listed parent class
class BaseHandler(tornado.web.RequestHandler, Sessionable):
    # edit this class to change all other RequestHandlers

    @gen.coroutine
    def prepare_child(self):
        pass

    @gen.coroutine
    def prepare(self):
        yield self.init_session(os.environ['DB_FQDN'])
        yield self.prepare_child()

    @gen.coroutine
    def on_finish_child(self):
        pass

    @gen.coroutine
    def on_finish(self):
        yield self.on_finish_child()


class AuthenticatedHandler(BaseHandler):
    def get_current_user(self):
        username = self.get_secure_cookie(
            'username',
            max_age_days=10
        )
        if username:
            return username.decode('ascii')
        else:
            return None


class HomeHandler(AuthenticatedHandler):
    def get(self):
        self.redirect('/dashboard')


class SettingsHandler(AuthenticatedHandler):
    @authenticated
    def get(self):
        ok = bool(int(self.get_argument('ok', '0')))
 
        self.render(
            'templates/settings.html',
            username=self.get_current_user(),
            ok=ok
        )


class PasswordHandler(AuthenticatedHandler):
    @authenticated
    @gen.coroutine
    def post(self):
        current = self.get_body_argument('current_password')
        new = self.get_body_argument('new_password')
        confirm = self.get_body_argument('confirm_new_password')
        if confirm != new:
            self.finish('new password must match confirm new password')
            return

        username = self.get_current_user()
        self.results = yield self.query(
            '''
            SELECT * FROM users
            WHERE username=%(username)s
            ''',
            {
                'username': username
            }
        )

        # valid login
        if not self.results or crypto.hash(
            current,
            username,
            self.results[0]['salt']
        ) != self.results[0]['hash']:
            self.finish('invalid username / old password incorrect')
            yield self.results.free()
            return

        new_hash = crypto.hash(
            new,
            username,
            self.results[0]['salt']
        )
        yield self.results.free()
        self.results = yield self.query(
            '''
            UPDATE users
            SET hash=%(hash)s
            WHERE username=%(username)s;
            ''',
            {
                'hash': new_hash,
                'username': username
            }
        )
        yield self.results.free()
        self.redirect('/settings?ok=1')


class DashboardHandler(AuthenticatedHandler):
    @authenticated
    def get(self):
        self.render(
            'templates/dashboard.html',
            username=self.get_current_user()
        )


class LogoutHandler(AuthenticatedHandler):
    def get(self):
        self.set_secure_cookie('username', '')
        self.redirect('/login')


class LoginHandler(AuthenticatedHandler):
    def get(self):
        self.render(
            'templates/login.html',
            bad_login=False
        )

    @gen.coroutine
    def post(self):
        username = self.get_body_argument('username')
        password = self.get_body_argument('password')
        self.results = yield self.query(
            '''
            SELECT * FROM users
            WHERE username=%(username)s
            ''',
            {
                'username': username
            }
        )

        if self.results and crypto.hash(
            password,
            username,
            self.results[0]['salt']
        ) == self.results[0]['hash']:
            # valid login
            self.set_secure_cookie(
                'username',
                username,
                expires_days=3
            )
            self.redirect('/')
        else:
            # invalid login
            yield gen.sleep(1)
            self.render(
                'templates/login.html',
                bad_login=True
            )

        yield self.results.free()


class SignupHandler(AuthenticatedHandler):
    def get(self):
        self.render(
            'templates/signup.html',
            bad_signup=False
        )

    @gen.coroutine
    def post(self):
        yield gen.sleep(0.5)

        username = self.get_body_argument('username')
        self.results = yield self.query(
            '''
            SELECT COUNT(*) FROM users
            WHERE username=%(username)s
            ''',
            {
                'username': username
            }
        )

        if self.results[0]['count']:
            yield self.results.free()

            # this username already exists
            self.render(
                'templates/signup.html',
                bad_signup=True
            )

        else:
            yield self.results.free()

            password = self.get_body_argument('password')
            salt = crypto.salt()
            user_id = crypto.user_id()
            user = {
                'user_id': user_id,
                'username': username,
                'salt': salt,
                'hash': crypto.hash(password, username, salt),
            }
            self.results = yield self.query(
                '''
                INSERT INTO users (
                    user_id,
                    username,
                    salt,
                    hash
                ) VALUES (
                    %(user_id)s,
                    %(username)s,
                    %(salt)s,
                    %(hash)s
                );
                ''',
                user
            )
            self.set_secure_cookie(
                'username',
                username,
                expires_days=3
            )
            self.redirect('/')


settings = {
    'cookie_secret': COOKIE_SECRET,
    'login_url': '/login',
    'debug': True
}


application = tornado.web.Application(
    [
        (r'/', HomeHandler),
        (r'/dashboard', DashboardHandler),
        (r'/settings', SettingsHandler),
        (r'/settings/password', PasswordHandler),
        (r'/signup', SignupHandler),
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler),
        (r'/images/(.+)', tornado.web.StaticFileHandler, {'path': './static/images/'}),
        (r'/css/(.+)', tornado.web.StaticFileHandler, {'path': './static/css/'}),
        (r'/js/(.+)', tornado.web.StaticFileHandler, {'path': './static/js/'}),
        (r'/(favicon\.ico)', tornado.web.StaticFileHandler, {'path': './favicons/'})
    ],
    **settings
)


if __name__ == '__main__':
    application.listen(port)
    print('starting tornado server on port %s' % port)
    tornado.ioloop.IOLoop().instance().start()
