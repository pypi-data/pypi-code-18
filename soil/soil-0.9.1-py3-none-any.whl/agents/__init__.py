# networkStatus = {}  # Dict that will contain the status of every agent in the network
# sentimentCorrelationNodeArray = []
# for x in range(0, settings.network_params["number_of_nodes"]):
#     sentimentCorrelationNodeArray.append({'id': x})
# Initialize agent states. Let's assume everyone is normal.
    

from .BaseBehaviour import *
from .BassModel import *
from .BigMarketModel import *
from .IndependentCascadeModel import *
from .ModelM2 import *
from .SentimentCorrelationModel import *
from .SISaModel import *
from .CounterModel import *
from .DrawingAgent import *
