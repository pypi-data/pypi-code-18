import sys
from stf.plugins.base_plugin import STFBasePlugin
from stf.lib.logging.logger import Logger
logger = Logger.getLogger(__name__)

class STFHtmlPlugin(STFBasePlugin):
    def __init__(self, plugins):
        super(STFHtmlPlugin, self).__init__(plugins)
        pass

    def run(self):
        logger.info("I AM running in html")

