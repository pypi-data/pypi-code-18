from twitter_controller.Text import Text
from twitter_controller.TwitterDownloader import TwitterDownloader


class Person:

    def __init__(self, name):
        self.twitter_id = id
        self.name = name
        self.texts = []
        self.downloader = TwitterDownloader()
        self.downloader.check_authentication()
        self.downloader.set_twitteruser(name)
        self.downloaded = False

    def get_texts(self):
        self._download_if_needed()
        return self.texts

    def all_text_as_one(self):
        self._download_if_needed()
        res = Text('')
        for t in self.texts:
            if t:
                res += t
        return res

    def get_profile_pict(self):
        return self.downloader.get_profilepict_url()

    def _download_if_needed(self):
        if not self.downloaded:
            print('Downloading tweets...')
            self.texts = self.downloader.download_all_tweets()
            self.downloaded = True
            print('Downloaded ' + str(len(self.texts)) + ' tweets')

    def get_tweetcontent_generator(self):
        for i in self.get_texts():
            yield(i.content)

    def get_name(self):
        return self.name