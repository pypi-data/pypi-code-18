import os

GIT_directory = '.git'
HEAD_FILE = 'HEAD'
ROOT = '/'


class GitDirectoryNotFoundException(Exception):
    def __init__(self, path=None):
        self.path = path or ''
        Exception.__init__(
            self,
            'Could not find a valid git directory at "{}"!'.format(self.path)
        )


class SearchParentDirectoryException(Exception):
    def __init__(self, path=None, search_depth=None):
        self.path = path or ''
        self.search_depth = search_depth or ''
        Exception.__init__(
            self,
            'Could not find a git directory in the parent '
            'directorys of "{}" (search depth="{}")!'.format(
                self.path, self.search_depth)
        )


class Repository:

    def __init__(
            self, path=None,
            search_parent_directories=False, max_search_depth=2):
        path = path or os.getcwd()
        self._search_parent_directories = search_parent_directories
        self._max_search_depth = max_search_depth

        self.branch = None
        self.revision = None

        if self._contains_git_directory(path):
            self._read_git_directory(os.path.join(path, GIT_directory))
        elif search_parent_directories:
            self._read_git_directory(self.find_git_directory(path))
        else:
            raise GitDirectoryNotFoundException(path)

    def _get_first_line(self, path):
        try:
            with open(path) as f:
                content = f.readlines()
                return content[0]
        except EnvironmentError:
            return None

    def _read_git_directory(self, path):
        head_file = os.path.join(path, HEAD_FILE)
        line = self._get_first_line(head_file)
        if not line:
            self.branch = None
            self.revision = None
        elif line.startswith('ref: '):
            prefix, ref_path = [s.strip() for s in line.split('ref: ')]
            ref_path = os.path.join(path, ref_path)
            self.branch = os.path.basename(ref_path)
            self.revision = (
                self._get_first_line(ref_path) or 'unknown').strip()
        else:
            self.branch = 'detached-head'
            self.revision = line.strip()

    def find_git_directory(self, start_path):
        path = start_path
        for i in range(self._max_search_depth):
            if path == ROOT:
                break
            if self._contains_git_directory(path):
                return os.path.join(path, GIT_directory)
            path = os.path.abspath(os.path.join(path, os.pardir))
        raise SearchParentDirectoryException(start_path, self._max_search_depth)

    def _contains_git_directory(self, path):
        if path is not None:
            git_path = os.path.join(path, GIT_directory)
            head_file = os.path.join(git_path, HEAD_FILE)
            return os.path.isdir(git_path) and os.path.isfile(head_file)
        return False

    @property
    def short_revision(self):
        if self.revision:
            return self.revision[:7]
        return None
