from flask import current_app as app
from flask import abort
from flask_login import current_user
from flask_login import login_required
from functools import wraps
from .initialise import get_access



# decorater can be used with @role_required('viewer')
def role_required(permission):
    def _role_required(func):
        @login_required
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            # if the login is off!
            if app.config.get('LOGIN_DISABLED'):
                return func(*args, **kwargs)
            access = get_access()
            if 'index' in kwargs:
                if kwargs['index'] not in access:
                    app.logger.debug('invalid channel <{0}> supplied'.format(kwargs['index']))
                    abort(403, "Invalid Channel")
                roles = access(kwargs['index'])(permission,set())
            else:
                roles = access.get('_default', {}).get(permission, set())

            if roles.isdisjoint(current_user.get_roles()):
                app.logger.debug('user does not have required roles for {0}'.format(permission))
                app.logger.debug(roles)
                app.logger.debug(current_user.get_roles())
                abort(403, 'insufficent priviledge for this function' )
            return func(*args, **kwargs)
        return func_wrapper
    return _role_required
