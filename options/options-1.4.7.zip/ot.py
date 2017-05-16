from options import *
from options.methset import *

class TestTwo(object):
    options = Options(this=1, that=1)

    def __init__(self, **kwargs):
        self.options = TestTwo.options.push(kwargs)

    @method_set
    def something(self, **kwargs):
        opts = method_push(self.options, self.something.__kwdefaults__, kwargs)
        return opts.this + opts.that

    @method_set
    def another(self, **kwargs):
        opts = method_push(self.options, self.another.__kwdefaults__, kwargs)
        return opts.this + opts.that

enable_method_set(TestTwo)

t = TestTwo()
print("-- done --")
