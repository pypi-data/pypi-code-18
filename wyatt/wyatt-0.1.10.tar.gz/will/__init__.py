import json, requests, sys, os, shutil
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

def send(message, name="annonymous", to="will"):
    data={'text': message, 'to': to, 'sender': name}
    code=requests.post(URL, data=json.dumps(data)).status_code
    if code==201:
        print('Sent message.')
    else:
        print('Failed to send message. %s'%code)

def get(quantity=5, offset=0):
    params={'limit': quantity, 'offset': offset, 'order_by': "-id"}
    print("Going to the server and getting files.")
    verify()
    return json.loads(requests.get(URL, params=params).text)['objects']

def stdout(message):
    sys.stdout.write(message)
    sys.stdout.write('\b' * len(message))
    
def display(objects):
    rows, columns = os.popen('stty size', 'r').read().split()
    objects.reverse()
    for msg in objects:
        print("%s%s%s,"%(bcolors.BOLD,msg['to'],bcolors.ENDC))
        print("  %s"%msg['text'])
        print("\t\t\t%s-%s%s"%(bcolors.OKBLUE,msg['sender'], bcolors.ENDC))
def get_update():
    r=requests.get("%sstatic/verify"%URL_BASE)
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
