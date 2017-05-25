from .compat import string_types
from .session import Session
from .endpoint import Endpoint, make_single_elem_property, make_single_elem_ref_property, make_multi_elem_ref_property


class Comment(Endpoint):

    ENDPOINT = '/comment'

    description = make_single_elem_property('comment', string_types, '', 'The text of the comment')
    created_by = make_single_elem_ref_property('userId', 'User', 'The user who added this comment', readonly=True)

    note = make_multi_elem_ref_property('nid', 'Note', 'The note this comment is attached to or None if not attached to a note')
    task = make_multi_elem_ref_property('tid', 'Task', 'The task this comment is attached to or None if not attached to a task')


Session.register_endpoint(Comment)
