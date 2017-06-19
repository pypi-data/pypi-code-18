import json

from rabbit import Rabbit
from rabbit import Sender

r = Rabbit()
r.connect()

queue_name = 'la_stampa'
binding_key = 'la_stampa'
exchange_name = 'news'

s = Sender(rabbit_instance=r,queue_name=queue_name)
s.bind(exchange_name=exchange_name,binding_key=binding_key)

message = {
    "category":"Sport",
    "fonte":"lastampa",
    "lista_news": [1,2,3,4,5,6,7,8,9]
}

body = json.dumps(message)
s.publish(binding_key,body)