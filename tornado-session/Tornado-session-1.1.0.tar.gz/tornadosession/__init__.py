import uuid
import hashlib
import redis
from tornado.websocket import WebSocketHandler
import time
try:
    import cPickle as pickle
except:
    import pickle


class SessionBaseHandler(WebSocketHandler):
    def initialize(self):
        self.session_config = self.settings.get("session")
        self.config_handle()
        try:
            self.redis = redis.StrictRedis(**self.session_config["driver_settings"])
        except Exception as e:
            print(e)

    def config_handle(self):
        self.cookie_config = {}
        if "expires" in self.session_config["cookie_config"]:
            self.cookie_config["expires"] = int(time.time()) + self.session_config["cookie_config"]["expires"]
        if "domain" in self.session_config["cookie_config"]:
            self.cookie_config["domain"] = self.session_config["cookie_config"]["domain"]
        if "httponly" in self.session_config["cookie_config"]:
            self.cookie_config["httponly"] = self.session_config["cookie_config"]["httponly"]
        if "secret" in self.session_config["cookie_config"]:
            self.application.settings["cookie_secret"] = self.session_config["cookie_config"]["secret"]

    @property
    def session_id(self):
        return self.get_secure_cookie("session_id") if self.get_secure_cookie("session_id") else self._generate_id()

    def get_current_user(self):
        return self.get_session()

    def _get_user(self, session_id):
        try:
            user_id = self.redis.get(session_id)
            raw_data = self.redis.get(user_id)
            if raw_data:
                user = pickle.loads(raw_data)
                return user
            else:
                return None
        except IOError:
            return None

    @staticmethod
    def _generate_id():
        temp = str(uuid.uuid4())
        new_id = hashlib.sha256(temp.encode("utf-8"))
        return new_id.hexdigest()

    def del_session(self):
        self.redis.delete(self.session_id)

    def get_session(self):
        session_id = self.get_secure_cookie("session_id")
        if session_id:
            user = self._get_user(session_id)
            if user:
                return user
        return None

    def set_session(self, user):
        session_data = pickle.dumps(user)
        session_id = self.session_id
        self.set_secure_cookie("session_id", session_id, **self.cookie_config)
        self.redis.set("user_{}".format(user.id), session_data)
        self.redis.set(session_id, "user_{}".format(user.id), ex=60 * 60 * 24)

    def refresh_session(self, user):
        session_data = pickle.dumps(user)
        self.redis.set("user_{}".format(user.id), session_data)