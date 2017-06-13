import os

CORPUS_DIR = os.path.expanduser('~/corpora')
UPLOAD_DIR = os.path.join(CORPUS_DIR, 'uploads')

# number of different words to show in pivot table
TOP_RESULTS = 50
# not respected yet.
MAX_TABLE_COLUMNS = 9999
MAX_TABLE_ROWS = 9999
MAX_CONC_COLUMNS = 9999
MAX_CONC_ROWS = 9999
# not working yet
THREADS = 3
# port to run app on if not specified manually
PORT = 5555
# number of decimal places to show in tables
DECIMALS = 3
# attempt to not make separate token for comma et al
COLLAPSE_TREE_PUNCTUATION = True


# USE MACOS NOTIFICATION CENTRE
USE_NOTIFICATIONS = True
# minimum time a search must take to attempt OS notification
NOTIFY_MIN_TIME = 10
# MAKE A NOISE WHEN NOTIFICATION OCCURS
NOTIFY_SOUND = False

# pre-load some tree json for quicker rendering
PREPARE_FIRST_N_TREES = 10

def get_secret_key():
    """
    Flask wants a unique ID for its session. This grabs a stable key,
    or, if not found, generates one.
    """
    f = os.path.expanduser('~/.flask.key')
    if os.path.isfile(f):
        with open(f, 'r') as fo:
            return fo.read().strip()
    else:
        return os.urandom(24)

# url for sample corpus file 1 and 2
UD_TRAIN = "https://raw.githubusercontent.com/UniversalDependencies/UD_English/master/en-ud-train.conllu"
UD_DEV = "https://raw.githubusercontent.com/UniversalDependencies/UD_English/master/en-ud-dev.conllu"
# where this corpus should go
UD_DIR = os.path.join(CORPUS_DIR, 'UD_English-parsed')