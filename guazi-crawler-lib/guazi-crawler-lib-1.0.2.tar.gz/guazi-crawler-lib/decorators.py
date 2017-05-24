# coding:utf8
'''
__author__ = 'chendansi'
created_at: 2017-05-22 14:15:00
'''



def error_handle(f):
    def func(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception, e:
            print 'func %s execute error:%s' % (f.__name__, str(e))
    return func


def retry(num):
    def return_func(f):
        def func(*args, **kwargs):
            for i in xrange(num):
                try:
                    return f(*args, **kwargs)
                    break
                except Exception, e:
                    print 'Func %s execute error:%s for %d times.' % (f.__name__, str(e), i+1)
        return func
    return return_func
