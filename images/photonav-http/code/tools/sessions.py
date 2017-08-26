import sys
from tornado import gen
from random import random
from queries.pool import PoolFullError
import tornado.web
from tornado import gen
import queries

import logging
logger = logging.getLogger(__name__)


class Sessionable:

    @gen.coroutine
    def init_session(self, db_fqdn):

        # makes cleanup easier later
        self.results = None

        self.session = queries.TornadoSession(
            db_fqdn,
            pool_max_size=200
        )

        try:
            validated = False
            while not validated:
                try:
                    yield self.session.validate()
                    validated = True

                except PoolFullError:
                    # no connections available yet
                    yield gen.sleep(1 + random())

        except Exception as error:
            logger.error('Error connecting to the database: %s' % error)
            raise tornado.web.HTTPError(503)


    @gen.coroutine
    def query(self, *args, **kwargs):
        validated = False
        while not validated:
            try:
                result = yield self.session.query(*args, **kwargs)
                return result
            except PoolFullError:
                # no connections available yet
                yield gen.sleep(1 + random())
