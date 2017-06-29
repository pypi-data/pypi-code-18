import logging

from nameko.standalone.rpc import ClusterRpcProxy
# from nameko_proxy.reply_listener import StandaloneReplyListener

from nameko_proxy.proxy import StandaloneRpcProxy
# from nameko_proxy import ClusterRpcProxy
# from eventlet.event import Event
from eventlet import monkey_patch

monkey_patch()

logging.basicConfig(level=logging.DEBUG)

config = {
    'AMQP_URI': 'pyamqp://10.10.7.7:30001',
}

# with ClusterRpcProxy(config, reply_listener_cls=StandaloneReplyListener) as rpc:
#     print(rpc.profiles_service.get_by_pid(1))

with StandaloneRpcProxy(config, context_data={'request_id': 111}) as rpc:
    # rpc.register_context_hook(lambda: {'request_id': 111})
    print(rpc.profiles_service.get_by_pid(2))


# e = Event()
# e.send('sss')
#
# print(e)
