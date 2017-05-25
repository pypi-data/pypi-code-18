from .session import Session
from .endpoint import Endpoint, make_single_readonly_property, make_multi_elem_ref_property


class User(Endpoint):

    ENDPOINT = '/user'

    LOAD_ALL = True

    name = make_single_readonly_property('user', '', 'User\'s name')
    email = make_single_readonly_property('email', '', 'User\'s email')

    is_owner = make_single_readonly_property('is_owner', False, 'Boolean indicator if the user is the owner of the Clevertim account')
    is_admin = make_single_readonly_property('is_admin', False, 'Boolean indicator if the user is an administrator of the Clevertim account')

    permissions = make_single_readonly_property('permissions', [], 'A list of permissions this user has')

    registration_pending = make_single_readonly_property('pending', False, 'True when the user has been invited to join Clevertim but has not yet joined, False if the user has registered')


class Group(Endpoint):

    ENDPOINT = '/group'

    LOAD_ALL = True

    name = make_single_readonly_property('name', '', 'Groups\'s name')
    gid = make_single_readonly_property('gid', '', 'Groups\'s id')
    users = make_multi_elem_ref_property('users', 'User', 'The list of users in this group', readonly=True)


Session.register_endpoint(User)
Session.register_endpoint(Group)
