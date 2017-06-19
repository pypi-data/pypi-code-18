class FoxtrotTextProcessor(object):
    def __init__(self, nextProcessor=None):
        self.nextProcessor = nextProcessor

    def process(self, text):
        if text == 'exit':
            raise Exception('Goodbye')
        return self.nextProcessor.process(text)


class FoxtrotQueryProcessor(object):
    def __init__(self, foxtrot_client, nextProcessor=None):
        self.foxtrot_client = foxtrot_client

    def process(self, query_text):
        return self.foxtrot_client.select(query_text)
