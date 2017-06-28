from dragline import runtime
import six
import time
from pytz import timezone
from datetime import datetime
from requests.compat import urlsplit
from six.moves import queue
from collections import defaultdict

from .http import Request, RequestError


class Crawler:
    def __init__(self):
        self.load()

    def load(self):
        redis_args = dict(host=runtime.settings.REDIS_URL,
                          port=runtime.settings.REDIS_PORT,
                          db=runtime.settings.REDIS_DB)
        if hasattr(runtime.settings, 'NAMESPACE'):
            redis_args['namespace'] = runtime.settings.NAMESPACE
        else:
            redis_args['namespace'] = runtime.spider.name
        self.url_set = set()
        self.url_queue = queue.Queue()
        runtime.stats = defaultdict(int)
        if not hasattr(runtime.spider, 'allowed_domains'):
            runtime.spider.allowed_domains = []
        self.delay = runtime.settings.MIN_DELAY
        if isinstance(runtime.spider.start, list):
            requests = runtime.spider.start
        else:
            requests = [runtime.spider.start]
        for request in requests:
            if isinstance(request, six.string_types):
                request = Request(request)
            if request.callback is None:
                request.callback = runtime.spider.parse
            self.insert(request)
        runtime.stats['start_time'] = self.current_time()

    def current_time(self):
        tz = timezone(runtime.settings.TIME_ZONE)
        return datetime.now(tz).isoformat()

    def clear(self, finished):
        runtime.stats['status'] = 'finished' if finished else 'stopped'
        runtime.stats['end_time'] = self.current_time()
        runtime.logger.info("%s", dict(runtime.stats))
        runtime.request_processor.clear()

    def insert(self, request, check=True):
        if not isinstance(request, Request):
            return
        url = urlsplit(request.url)
        if not all((url.scheme in ['http', 'https'], url.hostname)):
            runtime.logger.debug('invalid url %s', url.geturl())
            return
        reqhash = request.get_unique_id(True)
        if check:
            check = not request.dont_filter
        if check:
            if runtime.spider.allowed_domains and url.hostname not in runtime.spider.allowed_domains:
                runtime.logger.debug('invalid url %s (domain %s not in %s)', url.geturl(),
                                     url.hostname, str(runtime.spider.allowed_domains))
                return
            elif runtime.settings.UNIQUE_CHECK and reqhash in self.url_set:
                    return
        self.url_set.add(reqhash)
        self.url_queue.put(request)
        del request

    def updatedelay(self, delay):
        self.delay = min(
            max(runtime.settings.MIN_DELAY, delay,
                (float(self.delay) + delay) / 2.0),
            runtime.settings.MAX_DELAY)

    def process_request(self, request):
        response = request.send()
        if runtime.settings.AUTOTHROTTLE:
            self.updatedelay(response.elapsed.seconds)
            time.sleep(float(self.delay))
        runtime.stats['pages_crawled'] += 1
        runtime.stats["status_code:" + str(response.status)] += 1
        if len(response):
            runtime.stats['request_bytes'] += len(response)
        requests = request.callback(response)
        if requests:
            for i in requests:
                self.insert(i)
        return response

    def process_url(self):
        runtime.logger.info("Starting spider %s", dict(runtime.stats))
        while True:
            try:
                request = self.url_queue.get(timeout=2)
                runtime.logger.debug("Processing %s", request)
                self.process_request(request)
            except RequestError:
                request.retry += 1
                runtime.stats['retry_count'] += 1
                if request.retry >= runtime.settings.MAX_RETRY:
                    runtime.logger.warning("Rejecting %s and meta is %s", request, str(request.meta), exc_info=True)
                else:
                    runtime.logger.debug("Retrying %s", request, exc_info=True)
                    self.insert(request, False)
            except KeyboardInterrupt:
                self.insert(request, False)
                raise KeyboardInterrupt
            except queue.Empty:
                break
            except Exception:
                runtime.logger.exception("Failed to execute callback on %s and meta is %s", request, str(request.meta))
            else:
                runtime.logger.info("Finished processing %s", request)
