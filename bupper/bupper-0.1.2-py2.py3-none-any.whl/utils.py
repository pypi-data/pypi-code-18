import os
import datetime


def without_duplicates(iterable):
    seen = set()
    for item in iterable:
        if item not in seen:
            seen.add(item)
            yield item


def backup_filename_slug(path):
    '''
    Turn a filepath into a slug suitable for backup filenames.
    '''
    return (
        path.strip('/')
            .replace('--', '----')
            .replace('/', '--')
    )


def get_backup_archive_filename(date_format, path):
    '''
    Turn a date format and path to backup directory into the archive filename
    '''
    datetime_string = get_datetime_string(date_format)
    slug = backup_filename_slug(path)
    return '%s__%s.tar.gz' % (datetime_string, slug)


def makedirs_to(path):
    '''
    Make directories to include the given pathname
    '''
    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass


def get_datetime_string(date_format):
    '''
    Return `now' formatted with given format, with a special format of 'ISO'
    causing it to be formatted as ISO format excluding seconds.
    '''
    now = datetime.datetime.now()
    if date_format == 'ISO':
        datetime_string, _, _ = now.isoformat().rpartition(':')
    else:
        datetime_string = now.strftime(date_format)
    return datetime_string
