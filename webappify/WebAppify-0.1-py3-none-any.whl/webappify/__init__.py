"""
The :mod:`webapp` module contains a WebApp class which can be used to create simple "app windows"
for websites. To use it, do this::

  from webapp import WebApp

  app = WebApp('GMail', 'https://mail.google.com', 'gmail.png')
  app.run()

.. note:

   If your site needs Flash Player, you'll need the appropriate Flash Player plugin installed
   system-wide. For WebKit, this is the NPAPI plugin, and for WebEngine, this is the PPAPI plugin.

"""
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    from PyQt5 import QtWebEngineWidgets
    HAS_WEBENGINE = True
except ImportError:
    HAS_WEBENGINE = False

try:
    from PyQt5 import QtWebKit, QtWebKitWidgets
    HAS_WEBKIT = True
except ImportError:
    HAS_WEBKIT = False

if HAS_WEBENGINE:
    SETTINGS = [
        QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled,
        QtWebEngineWidgets.QWebEngineSettings.JavascriptCanAccessClipboard,
        QtWebEngineWidgets.QWebEngineSettings.LocalContentCanAccessRemoteUrls
    ]
    WebView = QtWebEngineWidgets.QWebEngineView
elif HAS_WEBKIT:
    SETTINGS = [
        QtWebKit.QWebSettings.AutoLoadImages,
        QtWebKit.QWebSettings.JavascriptEnabled,
        QtWebKit.QWebSettings.JavaEnabled,
        QtWebKit.QWebSettings.PluginsEnabled,
        QtWebKit.QWebSettings.JavascriptCanOpenWindows,
        QtWebKit.QWebSettings.JavascriptCanCloseWindows,
        QtWebKit.QWebSettings.JavascriptCanAccessClipboard,
        QtWebKit.QWebSettings.DeveloperExtrasEnabled,
        QtWebKit.QWebSettings.OfflineStorageDatabaseEnabled,
        QtWebKit.QWebSettings.OfflineWebApplicationCacheEnabled,
        QtWebKit.QWebSettings.LocalStorageEnabled,
        QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls,
        QtWebKit.QWebSettings.LocalContentCanAccessFileUrls,
        QtWebKit.QWebSettings.AcceleratedCompositingEnabled
    ]
    WebView = QtWebKitWidgets.QWebView
    class WebPage(QtWebKitWidgets.QWebPage):
        """Custom class for overriding the user agent to make WebKit look like Chrome"""
        def userAgentForUrl(self, url):
            return 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                   'Chrome/28.0.1500.52 Safari/537.36'
else:
    print('Cannot detect either QtWebEngine or QtWebKit!')
    sys.exit(1)


class WebWindow(QtWidgets.QWidget):
    """
    Window
    """
    def __init__(self, title, url, icon, parent=None):
        """
        Create the window
        """
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(icon))
        self.setContentsMargins(0, 0, 0, 0)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.webview = WebView(self)
        if HAS_WEBKIT:
            self.webview.setPage(WebPage(self.webview))
        for setting in SETTINGS:
            self.webview.settings().setAttribute(setting, True)
        self.webview.titleChanged.connect(self.onTitleChanged)
        self.webview.setUrl(QtCore.QUrl(url))
        self.layout.addWidget(self.webview)

    def onTitleChanged(self, title):
        """
        React to title changes
        """
        if title:
            self.setWindowTitle(title)


class WebApp(QtWidgets.QApplication):
    """
    A generic application to open a web page in a desktop app
    """
    def __init__(self, title, url, icon, hasTray=False, canMinimizeToTray=False):
        """
        Create an application which loads a URL into a window
        """
        super().__init__(sys.argv)
        self.beforeHooks = []
        self.afterHooks = []
        self.window = None
        self.title = title
        self.url = url
        self.icon = icon
        self.hasTray = hasTray
        self.canMinimizeToTray = canMinimizeToTray
        self.setWindowIcon(QtGui.QIcon(self.icon))

    def setupTrayIcon(self):
        """
        Set up the tray icon
        """
        if not QtWidgets.QSystemTrayIcon.isSystemTrayAvailable():
            # No reason to continue if the OS doesn't support system tray icons
            return
        self.trayIcon = QtWidgets.QSystemTrayIcon(QtGui.QIcon(self.icon), self.window)
        self.trayIcon.show()

    def addBeforeHook(self, hook):
        """
        Add a function to run before setting everything up
        """
        if hook:
            self.beforeHooks.append(hook)

    def run(self):
        """
        Run the app
        """
        self.window = WebWindow(self.title, self.url, self.icon)
        if self.hasTray:
            self.setupTrayIcon()
        self.window.showMaximized()
        return self.exec()
