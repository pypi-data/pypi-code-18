import random
import string
# ScriptContext import must be first!
from MoinMoin.web.contexts import ScriptContext
from MoinMoin import user
from MoinMoin.Page import Page
from MoinMoin.PageEditor import PageEditor
from MoinMoin import wikiutil

class PageExistsException(Exception):
    pass

def create_page(request, pagename, text):
    pagename = wikiutil.normalize_pagename(pagename, request.cfg)
    if Page(request, pagename).exists():
        raise PageExistsException(pagename + " already exists")
    else:
        editor = PageEditor(request, pagename)
        text = editor.normalizeText(text)
        dummy, revision, exists = editor.get_rev()
        editor.saveText(text, revision)

def create_user(request, username, password):
    """
    Create new user with the supplied details.
    An Exception is thrown if the user name or id already exists

    :return User: returns the valid (authenticated) new User
    """
    the_user = user.User(request, auth_method="new-user")
    the_user.name = unicode(username)
    the_user.enc_password = user.encodePassword(request.cfg, password)
    if (user.isValidName(request, the_user.name) and
            not user.getUserId(request, the_user.name)):
        the_user.save()
        new_user = user.User(request, name=username, password=password)
        assert new_user.valid == 1, "User is not valid"
        return new_user
    else:
        raise Exception("user credential already taken")

def pwd_gen(length=12, extended=False):
    charset = string.letters + string.digits
    if extended:
        charset += string.punctuation
    return ''.join(random.choice(charset) for i in range(length))
