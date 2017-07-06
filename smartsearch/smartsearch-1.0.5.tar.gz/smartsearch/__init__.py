# Builtin imports
import logging
import os
import json

# Internal imports
from smartsearch import exceptions, clients

# External imports
import nltk

_client_classes = {
    "wolfram": clients.Wolfram,
    "google": clients.Google
}

log = logging.getLogger()

# The required nltk corpora, from newspaper
REQUIRED_CORPORA = [
    'brown',  # Required for FastNPExtractor
    'punkt',  # Required for WordTokenizer
    'maxent_treebank_pos_tagger',  # Required for NLTKTagger
    'movie_reviews',  # Required for NaiveBayesAnalyzer
    'wordnet',  # Required for lemmatization and Wordnet
    'stopwords'
]

# Generate a list of all the modules that still need to be downloaded
not_downloaded = []

# The downloaded nltk modules
found = []
nltk_dirs = [
    "corpora",
    "tokenizers",
    "chunkers",
    "taggers"
]
for d in nltk_dirs:
    try:
        found += os.listdir(nltk.data.find(d))
    except LookupError:
        pass

for corpus in REQUIRED_CORPORA:
    corpus_name = "{}.zip".format(corpus)
    if corpus_name not in found:
        not_downloaded.append(corpus)


def nltk_download():
    """
    Download missing nltk modules required for the nlp functions in newspaper
    """
    log.info("{0} nltk modules required by the newspaper module have not been downloaded, downloading "
             "now.".format(len(not_downloaded)))
    for mod in not_downloaded:
        log.info("Downloading {}".format(mod))
        nltk.download(mod)


class Searcher:
    clients = {}
    keys = {}
    query_order = [
        "wolfram",
        "google"
    ]

    def __init__(self, keys=None, conf_file=None):
        """
        Instantiate a searcher object

        :param keys: A dictionary of keys and usage information for search clients
        :param conf_file: A configuration file to optionally load keys from
        """
        # Download the nltk modules required by newspaper that haven't been downloaded yet
        if not_downloaded:
            nltk_download()
        if conf_file:
            if os.path.isfile(conf_file):
                j = json.load(open(conf_file))
                self.keys = j
        else:
            self.keys = keys
        # Validate the API keys
        if keys:
            for key, key_data in self.keys.items():
                if key in _client_classes.keys():
                    if type(key_data) != str:
                        raise exceptions.InvalidKeyTypeError("Keys must be of type str")
        else:
            log.warning("No keys found")
        for client_name, client_baseclass in _client_classes.items():
            if client_baseclass.key_required:
                # If the client name is included in the loaded keys, instantiate the client with the key data.
                # If it's not included, warn in the logs that the client will be skipped
                if self.keys and client_name in self.keys.keys():
                    # Instantiate the client with the key information
                    instantiated_client = client_baseclass(self.keys[client_name])
                    self.clients.update({client_name: instantiated_client})
                    log.debug("Loaded client {0} with provided key information.".format(client_name))
                else:
                    log.warning("Skipping client {0} since it requires an api key that was not passed.".format(client_name))
            else:
                instantiated_client = client_baseclass()
                self.clients.update({client_name: instantiated_client})
                log.debug("Loaded client {0}.".format(client_name))

    @property
    def usages(self):
        usage_data = {}
        for client, client_class in self.clients.items():
            if client_class.key_required:
                usage_data.update(client.usages)
        return usage_data

    def query(self, query_text):
        for client in self.query_order:
            if client in self.clients.keys():
                resp = self.clients[client].query(query_text)
                if resp:
                    return resp
        # Raise an error if none of the clients found a result or completed without error
        raise exceptions.AllClientsFailedError("None of the enabled clients {0} could find an answer to the query "
                                               "{1}".format(", ".join(self.clients.keys()), query_text))

    def save(self, filename="search.conf"):
        """
        Save the current configuration to a file

        :param filename: The file to save it to. If none is specified, saved as "search.conf"
        """
        if self.keys:
            log.info("Caching search settings in file {}".format(filename))
            with open(filename, "w") as f:
                json_data = json.dumps(self.keys)
                f.write(json_data)
        else:
            log.warning("No configuration to cache")

