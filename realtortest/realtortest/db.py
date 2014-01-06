from scrapy import log
import hashlib
from redis import Redis
from redis.exceptions import ConnectionError

class Datastore(object):
    def __init__(self):
        try:
            self.conn = Redis(host="127.0.0.1", db=0)
        except:
            log.msg("WARNING could not connect to redis")
            self.conn = None  ## for testing
    def store(self, item):
        """
        we assume item comes in as a dict-compatible object
        """
        _id = hashlib.sha1("%s%s%s" % (item['street_address'],
                                       item['city'],
                                       item['region'])).hexdigest()
        log.msg(item)
        try:
            self.conn.hmset(_id, item)
        except ConnectionError:
            log.msg("ERROR could not connecto to redis db")
    def list(self):
        return map(lambda x: self.conn.hgetall(x), self.conn.keys())

datastore = Datastore()
