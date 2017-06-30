
from ws_callbacks import Callbacks

def test_call():
    cb = Callbacks()
    
    l = []

    def func1():
        l.append(1)
    
    def func2():
        l.append(2)
    
    cb.add_callback(func1)
    cb.add_callback(func2)
    
    cb()

    assert l == [1, 2]

