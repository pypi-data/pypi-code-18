from chatterbot import ChatBot
from pymongo import MongoClient


class ChatterbotUtils(object):
    def __init__(self, chatterbotcfg):
        self.chatterbotcfg = chatterbotcfg
        self.chatterbot = ChatBot(
            self.chatterbotcfg['name'],
            trainer="chatterbot.trainers.ChatterBotCorpusTrainer",
            input_adapter="chatterbot.input.VariableInputTypeAdapter",
            storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch'
                },
                {
                    'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                    'threshold': 0.65,
                    'default_response': self.chatterbotcfg['default_response']
                }
            ],
            database=self.chatterbotcfg['database'],
            read_only=self.chatterbotcfg['readonly'],
        )
        self.chatterbot.train("corpus")
        # self.drop_chatterbot_database()

    def drop_chatterbot_database(self):
        """Drop chatterbot database and train new one."""
        client = MongoClient(self.chatterbotcfg['host'], self.chatterbotcfg['port'])
        client.drop_database(self.chatterbotcfg['name'])
        self.chatterbot.train("corpus")

    def generate_chatterbot_response(self, message):
        """Generate chatterbot response"""
        return self.chatterbot.get_response(message)
