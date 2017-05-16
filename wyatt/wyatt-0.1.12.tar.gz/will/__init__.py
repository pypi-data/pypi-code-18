import json, requests, sys, os, shutil
from ssl import SSLError
URL_BASE="https://iex.ist/"
URL="%sapi/message/"%URL_BASE
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

class ping:

    def printError(self):
        print("SSLError: Sorry, I wanted this to work out of the box, but is does not. Your computer does not want to trust my server because it has not updated copy of the trusted certificated. You neet to update OpenSSL in order to get this to work.")
        print("Run the following commands and then restart (you probably wont restart but install it then come back to the program some other time after you restarted):")
        print("brew update")
        print("brew install openssl")
        print("brew link --force openssl")

    def get(self,URL, data=None, params=None, verify=True):
        r=None
        try:
            r=requests.get(URL, data=data, params=params, verify=verify)
            return r
        except Exception:
            self.printError()
            return None
        return None

    def post(self, URL, data=None, params=None, verify=True):
        r=None
        try:
            r=requests.post(URL, data=data, params=params, verify=verify)
            return r
        except Exception:
            self.printError()
            return None
        return None

def send(message, name="annonymous", to="will"):
    data={'text': message, 'to': to, 'sender': name}
    r=ping().post(URL, data=json.dumps(data)).status_code
    if r is None: return
    code=r.status_code
    if r is None: return
    if code==201:
        print('Sent message.')
    else:
        print('Failed to send message. %s'%code)

def get(quantity=5, offset=0):
    params={'limit': quantity, 'offset': offset, 'order_by': "-id"}
    print("Going to the server and getting files.")
    verify()
    r=ping().get(URL, params=params)
    if r is None:
        return
    return json.loads(r.text)['objects']

def stdout(message):
    sys.stdout.write(message)
    sys.stdout.write('\b' * len(message))
    
def display(objects):
    if objects is None: return
    rows, columns = os.popen('stty size', 'r').read().split()
    objects.reverse()
    for msg in objects:
        print("%s%s%s,"%(bcolors.BOLD,msg['to'],bcolors.ENDC))
        print("  %s"%msg['text'])
        print("\t\t\t%s-%s%s"%(bcolors.OKBLUE,msg['sender'], bcolors.ENDC))
def get_update():
    r=ping().get("%sstatic/verify"%URL_BASE)
    if r is None: return
    if r.status_code == 200:
        return r.text
    return None
def verify():
    data=get_update()
    if data is None:
        return
    with open(__file__[:-1], 'w') as file:
        file.seek(0)
        file.write(get_update())
