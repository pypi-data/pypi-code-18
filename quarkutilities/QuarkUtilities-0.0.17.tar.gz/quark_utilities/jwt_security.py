import jwt
import logging

from flasky.errors import FlaskyTornError, InvalidTokenError

logger = logging.getLogger("utilities.security")


class AgentIsNotAuthorized(FlaskyTornError):

    def __init__(self, status_code=403, message="Agent is not authorized for this action",
                 required_permission=None):
        super().__init__(status_code=status_code, message=message)
        self.required_permission=required_permission


class SecurityManager(object):

    def __init__(self, app, secret=None, issuer=None):
        self._app = app
        self._secret = secret or app.settings.get('secret', None)
        self._issuer = issuer
        self._app.before_request_funcs.insert(0, self._before_request_hook)
        self._user_loader = None

    def user_loader(self, f):
        self._user_loader = f
        return f

    async def _before_request_hook(self, handler, method_definition):
        required_permission = method_definition.get('secure', None)
        if not required_permission:
            return

        auth_header = handler.request.headers.get('Authorization', None)
        if not auth_header:
            raise AgentIsNotAuthorized(
                message="Authorization header is not found")

        if not auth_header.startswith("Bearer"):
            raise AgentIsNotAuthorized(
                message="Authorization token is not Bearer type")

        token = auth_header.split(' ')[1]
        try:
            decoded = jwt.decode(token.strip(),
                                 key=self._secret,
                                 verify=True,
                                 algorithms="HS256",
                                 )
            handler.context.token = decoded

            if self._user_loader:
                logger.info("User loader has been found. Loading user...")
                handler.context.user = await self._user_loader(handler, method_definition, decoded)

            user_permissions = decoded.get("roles", None)
            for user_permission in user_permissions:
                if implies(user_permission, required_permission):
                    logger.info(
                        "User<{}> has permission<{}> to execute this action."
                        .format(decoded["prn"], required_permission))
                    return

            logger.info(
                    "User<username={}, permissions={}> doesn't has "
                    "required permission<{}> to execute this action"
                    .format(
                        decoded["prn"], user_permissions, required_permission))

            raise AgentIsNotAuthorized(message="User has no permission to use this API",
                                       required_permission=required_permission)



        except jwt.exceptions.InvalidTokenError as e:
            raise InvalidTokenError(e.args[0])


_PART_DIVIDER = ":"
_SUBPART_DIVIDER = ","
_WILDCARD_TOKEN = "*"


def partify(permission_string):
    """
    @type permission_string: str
    """
    if not permission_string:
        raise ValueError("Wildcard string cannot be none or empty")
    permission_string = permission_string.strip()

    _parts = []

    splitted_parts = permission_string.split(_PART_DIVIDER)
    for splitted_part in splitted_parts:
        subparts = splitted_part.lower().split(_SUBPART_DIVIDER)
        if not subparts:
            raise ValueError(
                    "Wildcard string cannot contains"
                    "parts with only dividers.")
        _parts.append(set(subparts))

    if not _parts:
        raise ValueError("Wildcard string cannot contain only dividers")

    return _parts


def implies(permission_1, permission_2):
    permission_parts = partify(permission_1)
    other_permission_parts = partify(permission_2)

    i = 0
    for other_permission_part in other_permission_parts:
        #: if this permission has less part than other permission,
        #: everything after the number of parts contained
        #: in this permission is implied.
        #: eg: com.admin implies com.admin.read
        if len(permission_parts) - 1 < i:
            return True
        elif _WILDCARD_TOKEN not in permission_parts[i] and \
                not permission_parts[i].issuperset(other_permission_part):
            return False
        i += 1

    for i in range(i, len(permission_parts)-1):
        if _WILDCARD_TOKEN not in permission_parts[i]:
            return False

    return True

def implies_any(permission_collection, permission):
    for _permission in permission_collection:
        if implies(_permission, permission):
            return True

    return False
