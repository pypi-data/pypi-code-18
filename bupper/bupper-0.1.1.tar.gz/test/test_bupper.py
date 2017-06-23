'''
Tests for `bupper` module.
'''
import os
from os.path import join, exists
import tempfile
import datetime
from unittest.mock import patch

from bupper import bupper, utils

# '2017-02-03T04:05:06.000007'

MOCK_TIME = datetime.datetime(2017, 2, 3, 4, 5, 6, 7)


class MockTimeBase:
    @classmethod
    def setup_class(cls):
        cls.patcher = patch('datetime.datetime')
        mock_datetime = cls.patcher.start()
        mock_datetime.now.return_value = MOCK_TIME

    @classmethod
    def teardown_class(cls):
        bupper._is_verbose = False
        cls.patcher.stop()


class BlankEnvironBase:
    @classmethod
    def setup_class(cls):
        # Save & delete
        cls.patcher = patch('datetime.datetime')
        mock_datetime = cls.patcher.start()
        mock_datetime.now.return_value = MOCK_TIME
        cls.original_source = os.environ.get('BUPPER_SOURCE')
        if cls.original_source is not None:
            del os.environ['BUPPER_SOURCE']
        cls.original_dest = os.environ.get('BUPPER_LOCAL_BACKUP')
        if cls.original_source is not None:
            del os.environ['BUPPER_LOCAL_BACKUP']
        cls.original_bup = os.environ.get('BUPPER_REMOTE_BACKUP')
        if cls.original_bup is not None:
            del os.environ['BUPPER_REMOTE_BACKUP']

    @classmethod
    def teardown_class(cls):
        # Restore environmental variables
        if cls.original_source is not None:
            os.environ['BUPPER_SOURCE'] = cls.original_source
        if cls.original_dest is not None:
            os.environ['BUPPER_LOCAL_BACKUP'] = cls.original_dest
        if cls.original_bup is not None:
            os.environ['BUPPER_REMOTE_BACKUP'] = cls.original_bup
        bupper._is_verbose = False
        cls.patcher.stop()


class TestUtils(MockTimeBase):
    def test_without_duplicates(self):
        assert list(utils.without_duplicates('asdf')) == ['a', 's', 'd', 'f']
        assert list(utils.without_duplicates(
            'assddfsfddsfafdsa')) == ['a', 's', 'd', 'f']

    def test_bup_slug(self):
        bup_slug = utils.backup_filename_slug
        assert bup_slug('/asdf/jkl;') == 'asdf--jkl;'
        assert bup_slug('/asdf/test--dir/') == 'asdf--test----dir'
        assert bup_slug('/asdf/test----dir/') == 'asdf--test--------dir'

    def test_makedirs_to(self):
        # Make a directory tree
        d = tempfile.mkdtemp(prefix='tmp_bupper_test_')
        utils.makedirs_to(join(d, 'some/other/thing'))
        assert exists(join(d, 'some/other'))
        assert not exists(join(d, 'some/other/thing'))
        os.removedirs(join(d, 'some/other'))

    def test_get_datetime_string(self):
        get = utils.get_datetime_string
        assert get('ISO') == '2017-02-03T04:05'
        assert get('%Y test') == '2017 test'

    def test_get_backup_archive_filename(self):
        get = utils.get_backup_archive_filename
        assert get('ISO', '/asdf/jkl;') == \
            '2017-02-03T04:05__asdf--jkl;.tar.gz'
        assert get('lol', '/asdf/test--dir/') == \
            'lol__asdf--test----dir.tar.gz'


class TestParseArgs(BlankEnvironBase):
    def test_parse_args_default(self):
        args = bupper.parse_args([])
        assert args.source == '~'
        assert args.local == '/var/tmp/bupper/'
        assert args.remote is None
        assert args.date_format == 'ISO'
        assert not args.verbose

    def test_parse_args_all(self):
        args = bupper.parse_args([
            '-s', 'src',
            '-l', 'local',
            '-r', 'remotehost',
            '--verbose',
        ])
        assert args.source == 'src'
        assert args.local == 'local'
        assert args.remote == 'remotehost'
        assert args.verbose

    def test_environ_defaults(self):
        os.environ['BUPPER_SOURCE'] = 'src'
        os.environ['BUPPER_LOCAL_BACKUP'] = 'dest'
        os.environ['BUPPER_REMOTE_BACKUP'] = 'bup:~/'
        args = bupper.parse_args([])
        assert args.source == 'src'
        assert args.local == 'dest'
        assert args.remote == 'bup:~/'
        del os.environ['BUPPER_SOURCE']
        del os.environ['BUPPER_LOCAL_BACKUP']
        del os.environ['BUPPER_REMOTE_BACKUP']

    def test_check_args(self):
        args = bupper.parse_args(['-s', '~/stuff', '-v'])
        bupper.check_args(args)
        assert bupper._is_verbose
        # ensure expands home
        assert (
            'home' in args.source or  # linux
            'Users' in args.source    # macOS
        )


def write_tmp_file(path):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass
    open(path, 'w+').write('%s contents' % path)


def gen_tmp_files(root, files):
    for fn in files:
        write_tmp_file(join(root, fn))


def clear_tmp_files(root, files):
    for fn in files:
        path = join(root, fn)
        if exists(path):
            os.remove(path)
        try:
            os.removedirs(os.path.dirname(path))
        except OSError:
            pass


class TestPaths:
    def test_get_targets(self):
        # Test that it shows up when searching
        d = tempfile.mkdtemp(prefix='tmp_bupper_test_')
        os.makedirs(join(d, 'some/other'))

        # ensure it picks up on nothing
        assert list(bupper.get_targets(join(d))) == []

        # now check that it gets it correctly
        open(join(d, 'some/other/_BACKUP_THIS'), 'w+').write(' ')
        assert list(bupper.get_targets(join(d))) == [join(d, 'some/other')]

        # clean up test
        os.remove(join(d, 'some/other/_BACKUP_THIS'))
        os.removedirs(join(d, 'some/other'))


class TestPathGenerators:
    FILES = [
        '_vimrc',
        '_config/openbox/openbox.xml',
    ]

    @classmethod
    def setup_class(cls):
        cls.dir = tempfile.mkdtemp(prefix='tmp_bupper_test_')
        gen_tmp_files(cls.dir, cls.FILES)
        cls.results = set([
            (join(cls.dir, '_vimrc'),
                join('test_out', '.vimrc')),
            (join(cls.dir, '_config/openbox/openbox.xml'),
                join('test_out', '.config/openbox/openbox.xml')),
        ])

    @classmethod
    def teardown_class(cls):
        clear_tmp_files(cls.dir, cls.FILES + ['.vimrc'])


class TestFullBehavior(BlankEnvironBase):
    FILES = [
        'ignore_file_1',
        'example/ignore_file_2',

        'example/path/to/file_1',
        'example/path/to/file_2',
        'example/path/to/nested/file_1',
        'example/path/to/_BACKUP_THIS',

        'other/backup/file_1',
        'other/backup/_BACKUP_THIS',
    ]

    def setup_method(self, method):
        self.source_dir = tempfile.mkdtemp(prefix='tmp_bupper_test_SRC_')
        self.local_dir = tempfile.mkdtemp(prefix='tmp_bupper_test_LOCAL_')
        self.remote_dir = tempfile.mkdtemp(prefix='tmp_bupper_test_REMOTE_')
        gen_tmp_files(self.source_dir, self.FILES)

    def test_backup_unmocked_commands(self):
        bupper.main(bupper.parse_args([
            '-s', self.source_dir,
            '-l', self.local_dir,
            '-r', self.remote_dir,
        ]))
        local_dir_contents = os.listdir(self.local_dir)
        remote_dir_contents = os.listdir(self.remote_dir)
        assert len(local_dir_contents) == 4
        assert len(remote_dir_contents) == 2
        local_fns = [fn for fn in local_dir_contents if fn.startswith('2017')]
        assert set(local_fns) == set(remote_dir_contents)
        path_1 = join(self.source_dir, 'example/path/to')
        path_2 = join(self.source_dir, 'other/backup')
        assert set(local_fns) == set([
            utils.get_backup_archive_filename('ISO', path_1),
            utils.get_backup_archive_filename('ISO', path_2),
        ])

    def teardown_method(self, method):
        clear_tmp_files(self.source_dir, self.FILES)
        local_dir_contents = os.listdir(self.local_dir)
        remote_dir_contents = os.listdir(self.remote_dir)
        clear_tmp_files(self.local_dir, local_dir_contents)
        clear_tmp_files(self.remote_dir, remote_dir_contents)
