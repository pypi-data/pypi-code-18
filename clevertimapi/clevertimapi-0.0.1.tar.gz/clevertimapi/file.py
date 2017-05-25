from .compat import string_types
from .session import Session
from .endpoint import Endpoint, make_single_elem_property, make_single_readonly_property, make_single_elem_ref_property, ValidationError


def is_folder_saved(folder):
    if folder.is_new():
        raise ValidationError("The parent property needs to be a saved Folder. Call save() on the Folder before assigning it to the parent property.")
    return True


class Folder(Endpoint):

    ENDPOINT = '/folder'

    DEFAULTS = {
        'is_dir': True
    }

    name = make_single_elem_property('name', string_types, '', 'Folder name')
    parent = make_single_elem_ref_property('parentId', 'Folder', 'The parent folder or None if within the root folder', validate_func=is_folder_saved)


class File(Endpoint):

    ENDPOINT = '/file'

    name = make_single_elem_property('name', string_types, '', 'File name')
    parent = make_single_elem_ref_property('parentId', 'Folder', 'The parent folder or None if within the root folder', validate_func=is_folder_saved)


class LinkedFile(Endpoint):

    ENDPOINT = '/linkedfile'

    class LINKED_SYSTEM(object):
        DROPBOX = 'D'
        GOOGLEDRIVE = 'G'

    name = make_single_elem_property('name', string_types, '', 'File name')
    storage_system = make_single_readonly_property('sys', doc_string='The external system where this file is stored (i.e. Dropbox, Google Drive)')
    size = make_single_readonly_property('size', default=0, doc_string='The size of the file in bytes')
    file_url = make_single_readonly_property('link', doc_string='The link/url to the file in the external system (i.e. Dropbox, Google Drive)')
    icon_url = make_single_readonly_property('icon', doc_string='The link/url to the icon for this file in the external system (i.e. Dropbox, Google Drive)')


Session.register_endpoint(Folder)
Session.register_endpoint(File)
Session.register_endpoint(LinkedFile)
