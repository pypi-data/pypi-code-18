import ast
import tokenize

from sys import stdin

__version__ = '1.1'

LIBFAKETIME_ERROR_CODE = 'T004'
LIBFAKETIME_ERROR_MESSAGE = 'import of fake_time from libfaketime found (should be from libfaketime_tz_wrapper)'


class LibfaketimeChecker(object):
    name = 'flake8-libfaketime'
    version = __version__

    def __init__(self, tree, filename='(none)', builtins=None):
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
            if (isinstance(node, ast.ImportFrom) and node.module == 'libfaketime' and 'fake_time' in [alias.name for alias in node.names]) or \
               (isinstance(node, ast.Import) and 'libfaketime' in [alias.name for alias in node.names]) and \
               node.lineno not in noqa:
                errors.append({
                    "message": '{0} {1}'.format(LIBFAKETIME_ERROR_CODE, LIBFAKETIME_ERROR_MESSAGE),
                    "line": node.lineno,
                    "col": node.col_offset
                })

        # Yield the found errors
        for error in errors:
            yield (error.get("line"), error.get("col"), error.get("message"), type(self))


def _get_noqa_lines(code):
    tokens = tokenize.generate_tokens(lambda L=iter(code): next(L))
    return [token[2][0] for token in tokens if token[0] == tokenize.COMMENT and
            (token[1].endswith('noqa') or (isinstance(token[0], str) and token[0].endswith('noqa')))]
