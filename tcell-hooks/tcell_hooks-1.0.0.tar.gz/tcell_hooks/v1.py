LOGIN_SUCCESS = "success"
LOGIN_FAILURE = "failure"


""" Report a Login event by providing all the necessary parameters for a TCell event
#
# ==== Examples
#  from tcell_hooks.v1 import LOGIN_SUCCESS, LOGIN_FAILURE, send_login_event
#
#  send_login_event(
#    status=LOGIN_SUCCESS,
#    session_id="124KDJFL3234",
#    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) ...",
#    referrer="http://192.168.99.100:3000/",
#    remote_address="192.168.99.1",
#    header_keys=["HOST", "USER_AGENT", "ACCEPT", "REFERER", "ACCEPT_ENCODING", "ACCEPT_LANGUAGE", "COOKIE"],
#    user_id="tcell@tcell.io",
#    document_uri="/users/auth/doorkeeper/callbackuri"
#  )
#
#  send_login_event(
#    status=LOGIN_FAILURE,
#    session_id="124KDJFL3234",
#    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) ...",
#    referrer="http://192.168.99.100:3000/",
#    remote_address="192.168.99.1",
#    header_keys=["HOST", "USER_AGENT", "ACCEPT", "REFERER", "ACCEPT_ENCODING", "ACCEPT_LANGUAGE", "COOKIE"],
#    user_id="tcell@tcell.io",
#    document_uri="/users/auth/doorkeeper/callbackuri"
#  )
"""
def send_login_event(status,
                     session_id,
                     user_agent,
                     referrer,
                     remote_address,
                     header_keys,
                     user_id,
                     document_uri,
                     user_valid=None):
    pass


""" Report a Login event by providing a Flask request object
#
# ==== Examples
#
#  from tcell_hooks.v1 import LOGIN_SUCCESS, LOGIN_FAILURE, send_flask_login_event
#
#  send_flask_login_event(
#    status=LOGIN_SUCCESS,
#    flask_request=request,
#    user_id="tcell@tcell.io",
#    session_id="124KDJFL3234"
#  )
#
#  send_flask_login_event(
#    status=LOGIN_FAILURE,
#    flask_request=request,
#    user_id="tcell@tcell.io",
#    session_id="124KDJFL3234"
#  )
"""
def send_flask_login_event(status,
                           flask_request,
                           user_id,
                           session_id,
                           user_valid=None):
    pass


""" Report a Login event by providing a Django request object
#
# ==== Examples
#
#  from tcell_hooks.v1 import LOGIN_SUCCESS, LOGIN_FAILURE, send_django_login_event
#
#  send_django_login_event(
#    status=LOGIN_SUCCESS,
#    django_request=request,
#    user_id="tcell@tcell.io",
#    session_id="124KDJFL3234"
#  )
#
#  send_django_login_event(
#    status=LOGIN_FAILURE,
#    django_request=request,
#    user_id="tcell@tcell.io",
#    session_id="124KDJFL3234"
#  )
"""
def send_django_login_event(status,
                            django_request,
                            user_id,
                            session_id,
                            user_valid=None):
    pass
