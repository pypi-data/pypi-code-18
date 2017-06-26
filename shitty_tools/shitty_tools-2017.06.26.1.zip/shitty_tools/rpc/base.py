import threading


def register(call_queue, response_queue, function):
    def worker_thread():
        while True:
            function_args, function_kwargs = call_queue.get()
            try:
                result = function(*function_args, **function_kwargs)
                response_queue.put((None, result))
            except Exception as e:
                response_queue.put((e, None))

    t = threading.Thread(target=worker_thread)
    t.daemon = True
    t.start()

    return get_proxy_function(call_queue, response_queue)


def get_proxy_function(call_queue, response_queue):
    def call(*args, **kwargs):
        call_queue.put((args, kwargs))
        e, result = response_queue.get()
        if e:
            raise e
        return result
    return call



class base_proxy(object):
    def __init__(self, output_function, input_function):
        self.output_function = output_function
        self.input_function = input_function

    def __call__(self, *args, **kwargs):
        pass