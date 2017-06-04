import random
import re

import indicoio
from twitter_controller.Plotter import Factor, Plotter
from twitter_controller.TwitterDownloader import TwitterDownloader, TwitterDownloaderException
from indicoio import IndicoError

from ENV import APIs
import os

class PersonAnalyzer:
    LANGUAGE = 'english'
    AMOUNT_OF_FACTORS = 7
    TRUSTED_SOURCE = os.path.dirname(__file__) + '/resources/TrustedSources'
    NOTTRUSTED_SOURCE = os.path.dirname(__file__) + '/resources/NotTrustedSources'

    def __init__(self, person):
        print(self.TRUSTED_SOURCE)
        self.person = person
        indicoio.config.api_key = APIs.indicoio
        self.political_stats = None
        self.personality_stats = None
        self.personas_stats = None
        self.emotions_stats = None
        self.profile_pict_stats = None
        self.plotter = Plotter(common_name=person.get_name())
        self._check_resources()

    def full_analyze(self, links_to_check=30):
        i = 1
        self.analyze_tweets_politicaly()
        print('Analysing... ' + str(round(i / self.AMOUNT_OF_FACTORS, 4) * 100) + '%')
        i += 1
        self.analyze_tweets_personality()
        print('Analysing... ' + str(round(i / self.AMOUNT_OF_FACTORS, 4) * 100) + '%')
        i += 1
        self.analyze_tweets_personas()
        print('Analysing... ' + str(round(i / self.AMOUNT_OF_FACTORS, 4) * 100) + '%')
        i += 1
        self.analyze_tweets_emotions()
        print('Analysing... ' + str(round(i / self.AMOUNT_OF_FACTORS, 4) * 100) + '%')
        i += 1
        self.analyze_profile_pict()
        print('Analysing... ' + str(round(i / self.AMOUNT_OF_FACTORS, 4) * 100) + '%')
        i += 1
        self.analyze_links(amount=links_to_check)
        print('Analysing... 100%')

    def analyze_tweets_politicaly(self):
        try:
            self.political_stats = Factor(indicoio.political(self.person.all_text_as_one().content).items(),
                                          'Political stats')
            self.plotter.add_factor(self.political_stats)
        except IndicoError:
            raise PersonAnalyzerException('Error while fetching data from indicoio')

    def analyze_tweets_personality(self):
        try:
            self.personality_stats = Factor(indicoio.personality(self.person.all_text_as_one().content).items(),
                                            'Personality stats')
            self.plotter.add_factor(self.personas_stats)
        except IndicoError:
            raise PersonAnalyzerException('Error while fetching data from indicoio')

    def analyze_tweets_personas(self):
        try:
            self.personas_stats = Factor(indicoio.personas(self.person.all_text_as_one().content).items(),
                                         'Personas stats')
            self.plotter.add_factor(self.personas_stats)
        except IndicoError:
            raise PersonAnalyzerException('Error while fetching data from indicoio')

    def analyze_tweets_emotions(self):
        try:
            self.emotions_stats = Factor(indicoio.emotion(self.person.all_text_as_one().content).items(),
                                         'Emotions stats')
            self.plotter.add_factor(self.emotions_stats)
        except IndicoError:
            raise PersonAnalyzerException('Error while fetching data from indicoio')

    def analyze_profile_pict(self):
        try:
            self.profile_pict_stats = Factor(indicoio.fer(self.person.get_profile_pict()).items(),
                                             'Profile picture emotions stats')
            self.plotter.add_factor(self.profile_pict_stats)
        except IndicoError:
            raise PersonAnalyzerException('Error while fetching data from indicoio')

    def plot_all(self):
        self.plotter.plot_all()

    def analyze_links(self, amount=30):
        '''
        Analyzes up to amount of links. The amount can be lower because of connection error to some sites
        or because this user did not post amount links.
        :param amount: amount of links to process
        '''
        final_amount = amount
        try:
            print('Analyzing links...')
            links = self.person.all_text_as_one().get_external_links()
            links = random.sample(set(links), min(amount, len(links)))


            # links = list(map(lambda l: TwitterDownloader._unshorten_url(l), links))

            unshortened = []
            for l in links:
                try:
                    unshortened.append(TwitterDownloader._unshorten_url(l))
                except TwitterDownloaderException:
                    final_amount -= 1
            links = unshortened

            with open(self.TRUSTED_SOURCE) as f:
                trusted = f.readlines()
            with open(self.NOTTRUSTED_SOURCE) as f:
                nottrusted = f.readlines()

            trusted_no = self._count_links(trusted, links)
            nottrusted_no = self._count_links(nottrusted, links)
            neutral_no = len(links) - trusted_no - nottrusted_no
            self.plotter.add_factor(Factor([('trusted', trusted_no), ('not trusted', nottrusted_no), ('not known', neutral_no)],
                                           'Links liability stats (' + str(final_amount) + ' random links)'))
        except FileNotFoundError:
            raise PersonAnalyzerException('File with resources could not be found')

    def _check_resources(self):
        try:
            with open(self.TRUSTED_SOURCE) as f:
                pass
            with open(self.NOTTRUSTED_SOURCE) as f:
                pass
        except FileNotFoundError:
            raise PersonAnalyzerException('File with resources could not be found')

    @staticmethod
    def _count_links(control, tested):
        res = 0
        for l in tested:
            for c in control:
                if re.match('http[s]?://(www\.)?' + c + '(/*)(.*)', l):
                    res += 1
                    break
        return res


class PersonAnalyzerException(Exception):
    pass