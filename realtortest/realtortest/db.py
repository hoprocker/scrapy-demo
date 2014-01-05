import hashlib
from redis import Redis

class Datastore(object):
    def __init__(self):
        self.conn = Redis(host="127.0.0.1", db=0)
    def store(self, item):
        """
        we assume item comes in as a dict-compatible object
        """
        _id = hashlib.sha1("%s%s%s" % (item['street_address'],
                                       item['city'],
                                       item['region'])).hexdigest()
        self.conn.hmset(_id, item)
    def list(self):
        return map(lambda x: self.conn.hmget(x), self.conn.keys())

datastore = Datastore()
