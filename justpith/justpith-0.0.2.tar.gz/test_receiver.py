from rabbit import Rabbit
from rabbit import Receiver

r = Rabbit()
r.connect()

queue_name = 'la_stampa'
binding_key = 'la_stampa'
exchange_name = 'news'


rec = Receiver(r,queue_name)
rec.bind(exchange_name,binding_key)
rec.consume()