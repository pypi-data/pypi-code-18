import urllib2
import urllib
import json

class TelegramBot(object):

    def __init__(self, token):
        self.token = token

    def read_message(self):
        uri = 'https://api.telegram.org/bot{token}/getUpdates'.format(token=self.token)
        response = urllib2.urlopen(uri)
        data = response.read()
        data = json.loads(data)

        data_tele= data['result'][0]
        if len(data)>0:
            data_json = "{sender}|{chat_id}|{message}".format(sender=data_tele['message']['chat']['username'],chat_id=data_tele['message']['chat']['id'],message=data_tele['message']['text'])

            urllib2.urlopen('https://api.telegram.org/bot{token}/getUpdates?offset={offset}'.format(token=self.token,offset=int(data['result'][0]['update_id'])+1))
            return data_json
        else:
            return "None"

    def send_message(self, msg,chat_id):
        text_encoded = urllib.quote_plus(msg)
        #chat_id = '180768676'
        chat_id = chat_id
        uri = 'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={isi}'.format(chat_id=chat_id, token=self.token, isi=text_encoded)
        response = urllib2.urlopen(uri)

    def get_chat_id(self):
        data = self.read_message()
        for i in data:
            data

        return data
# okay decompyling tele.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.04.15 22:16:45 WIB
