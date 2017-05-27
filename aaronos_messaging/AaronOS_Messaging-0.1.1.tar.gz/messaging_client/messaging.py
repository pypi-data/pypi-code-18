import requests, re
from messaging_client.fix_json import fix_lazy_json
from ast import literal_eval

class Messaging(object):
    """
    Python client for Aaron-OS Messaging
    """
    def __init__(self, username, is_admin):
        if is_admin:
            # Adding "{ADMIN} " to the front of your name makes you admin
            self.username = "{ADMIN} " + username
        else:
            self.username = username

        #Setup URL
        self.url = "http://aaron-os-mineandcraft12.c9.io/"
        self.get_message_url = self.url + "messaging.php"
        self.put_message_url = self.url + "messager.php"

        #Get id of last message
        self.last_message_id = 0
        self.poll()

    def _parse_response(self, response):
        fixed_plain = fix_lazy_json(response).strip()
        dict_response = literal_eval(fixed_plain)
        dict_response["l"] = int(dict_response["l"])
        return dict_response

    def send_message(self, content):
        payload = {"n":self.username, "c":content}
        #Doesn't return anything so no need to save
        requests.get(self.put_message_url, params=payload)

    def get_message(self, message_id):
        #For some reason returns message_id + 1
        message = requests.get(self.get_message_url, params={"l":message_id})
        message = self._parse_response(message.text)
        return message

    def poll(self):
        #Check for new messages
        check = self.get_message(-1)

        if int(check["l"])+1 != self.last_message_id:
            #Get latest message
            #For some reason l = l + 1
            latest = self.get_message(int(check["l"]))
            self.last_message_id = latest["l"]
            return {"new":True, "content":latest}

        return {"new":False, "content":check}