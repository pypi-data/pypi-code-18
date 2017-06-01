from threading import Thread

from etcd import EtcdWatchTimedOut
from etcd.client import Client as ETCDClient
from .within_template_config import confer_instance

try:
  from queue import queue as Queue, Empty
except ImportError:
  from Queue import Queue, Empty


class TemplateApi:
  def __init__(self, watch_timeout, auto_add_watches, endpoints):
    if endpoints is None:
      endpoints = [('localhost', 2379)]
    self.etcd_cli = ETCDClient(
        host=endpoints,
        allow_reconnect=True
    )
    self.watch_timeout = watch_timeout
    self.auto_add_watches = auto_add_watches

  def get_key(self, key):
    if self.auto_add_watches:
      confer_instance.watched_keys.append(key)
    return self.etcd_cli.get(key).value

  def watch_keys(self, keys):
    print('Watching keys {}'.format(keys))
    q = Queue()

    def watch_and_notify(key):
      try:
        self.etcd_cli.watch(key, timeout=self.watch_timeout)
      except EtcdWatchTimedOut:
        pass
      q.put(True)

    for key in keys:
      t = Thread(target=watch_and_notify, args=(key,))
      t.daemon = True
      t.start()
    try:
      q.get(block=True, timeout=self.watch_timeout)
    except Empty:
      pass


_instance = None


def get_key(key):
  return _instance.get_key(key)


def watch_keys(keys):
  return _instance.watch_keys(keys)


def setinstance(
    watch_timeout=60,
    auto_add_watches=True,
    endpoints=None
  ):
  global _instance
  _instance = TemplateApi(
      watch_timeout=watch_timeout,
      auto_add_watches=auto_add_watches,
      endpoints=endpoints
  )
