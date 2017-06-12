from threading import local

__version__ = '0.4'

__thread_locals = local()


def get_current_user():
    return getattr(__thread_locals, 'emtex_user', 'AnonymousUser')


def set_current_user(user_email):
    setattr(__thread_locals, 'emtex_user', user_email)
