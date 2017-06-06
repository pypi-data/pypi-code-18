import sys
from nbconvert import Exporter
from .challenges import *


CHALLENGES = {'coding': make_coding,
              'multiple_choice': make_multiple_choice,
              'paragraph': make_paragraph,
              'number': make_number,
              'raw': make_raw,
}


class LearnExporter(Exporter):
    output_mimetype = 'application/newformat'

    def _file_extension_default(self):
        return '.md'

    def from_notebook_node(self, nb, resources=None):
        import uuid
        nb_fname = sys.argv[-1]
        challenge_name, challenge_type, md, ipynb = nb_fname.split('.')
        make_challenge = CHALLENGES[challenge_type]
        uuid = uuid.uuid4()
        markdown = make_challenge(nb, str(uuid))

        return markdown, resources
