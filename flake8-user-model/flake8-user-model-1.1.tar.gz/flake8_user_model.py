import ast
import tokenize

from sys import stdin

__version__ = '1.1'

USER_MODEL_ERROR_CODE = 'T007'
USER_MODEL_ERROR_MESSAGE = 'user model import found'


class UserModelImportsChecker(object):
    name = 'flake8-user-model'
    version = __version__
    ignores = ()

    def __init__(self, tree, filename='(none)'):
        self.tree = tree
        self.filename = (filename == 'stdin' and stdin) or filename

    def run(self):
        # Get lines to ignore
        if self.filename == stdin:
            noqa = _get_noqa_lines(self.filename)
        else:
            with open(self.filename, 'r') as file_to_check:
                noqa = _get_noqa_lines(file_to_check.readlines())

        # Run the actual check
        errors = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ImportFrom) and node.module == 'django.contrib.auth.models' and 'User' in [alias.name for alias in node.names] and node.lineno not in noqa:
                errors.append({
                    'message': '{0} {1}: {2}'.format(USER_MODEL_ERROR_CODE, USER_MODEL_ERROR_MESSAGE, node.names[0].name),
                    'line': node.lineno,
                    'col': node.col_offset,
                })

        # Yield the found errors
        for error in errors:
            yield (error.get("line"), error.get("col"), error.get("message"), type(self))


def _get_noqa_lines(code):
    tokens = tokenize.generate_tokens(lambda L=iter(code): next(L))
    return [token[2][0] for token in tokens if token[0] == tokenize.COMMENT and
            (token[1].endswith('noqa') or (isinstance(token[0], str) and token[0].endswith('noqa')))]
