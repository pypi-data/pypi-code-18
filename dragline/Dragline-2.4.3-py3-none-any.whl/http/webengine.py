import sys
import time
from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtCore import QUrl


class NWUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, headers):
        super().__init__()
        self.headers = headers

    def set_headers(self, headers):
        self.headers = headers

    def interceptRequest(self, info):
        print(info.requestMethod())
        # for header in self.headers:
        #    info.setHttpHeader(header, self.headers[header])


class Render(QWebEngineView):
    def __init__(self, url, callback):
        self.callback = callback
        self.html = None
        self.app = QApplication(sys.argv)
        QWebEngineView.__init__(self)
        self.loadFinished.connect(self._loadFinished)
        self.load(QUrl(url))
        self.show()
        self.app.exec_()

    def _callable(self, data):
        self.html = data

    def _loadFinished(self, result):
        # self.page().toHtml(self._callable)
        self.loadFinished.disconnect()
        self.callback(self)
        # Data has been stored, it's safe to quit the app

    def fill(self, eid, data):
        script = 'document.getElementById("{}").value = "{}"'.format(eid, data)
        self.page().runJavaScript(script, lambda x: print(x))

    def click(self, eid):
        script = 'document.getElementById("{}").click()'.format(eid)
        self.page().runJavaScript(script, lambda x: print(x))

    def close(self):
        self.app.quit()


class Response:
    def __init__(self, text, status):
        self.status_code = status
        self.text = text

    @property
    def status(self):
        return self.status_code

    def clear(self):
        pass

    def __len__(self):
        return len(self.text)


# class RequestProcessor:
#     def get_response(self, **kwargs):
#         return render(kwargs['url'], kwargs['callback'])

#     def clear(self):
#         pass
