import logging
import logging.handlers
import slackweb

class SlackHandler(logging.Handler):
    def __init__(self, url, channel):
        logging.Handler.__init__(self)
        self.slack = slackweb.Slack(url=url)
        self.channel = channel

    def emit(self, record):
        try:
            payload = self.format(record)
            self.slack.notify(text=payload, channel=self.channel)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
