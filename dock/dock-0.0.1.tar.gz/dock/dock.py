import redis
import uuid
import ujson as json


class Dock:

    def __init__(self, name, **redis_kwargs):
        """
        Arguments:
            name (str): name of the queue.
            redis_kwargs (dict): arguments for `redis.Redis`.
        """
        self.db = redis.Redis(**redis_kwargs)
        self.send_addr = "dock:" + name + ":pending"
        self.recv_addr = "dock:" + name + ":done:{id}"

    def __len__(self):
        """
        Returns:
            how many items are in the queue.
        """
        return self.db.llen(self.send_addr)

    def empty(self):
        """
        Returns:
            whether the queue is empty.
        """
        return len(self) == 0

    def send(self, item, timeout=30):
        """
        Arguments:
            item (dict): item to queue up.
            timeout (int): if no response in this many seconds, then give up.

        Returns:
            if timed out, then returns None.
            otherwise returns a `dict` corresponding to the response.
        """
        uid = str(uuid.uuid4().int & (1<<64)-1)
        msg = {'id': uid, 'msg': item}
        self.db.rpush(self.send_addr, json.dumps(msg))
        key, resp = self.db.blpop(self.recv_addr.format(id=uid), timeout=30)
        if resp:
            return json.loads(resp.decode())
        else:
            return None

    def recv(self):
        """
        Returns:
            a tuple of `(dict, function)`, corresponding to the dequeued item and a function with which to send back a response.
        """
        key, incoming = self.db.blpop(self.send_addr)
        d = json.loads(incoming.decode())
        uid, msg = d['id'], d['msg']
        def respond(response):
            self.db.rpush(self.recv_addr.format(id=uid), json.dumps(response))
        return msg, respond
