# -*- coding: utf-8 -*-

"""
Scans given directory, adds to calibre all books which are not yet
present there. Duplicate checking is done solely on file content
comparison (file name may differ).  Used to double-check whether some
dir items were already added to calibre.

Example:

    calibre_add_if_missing /home/jan/OldBooks

(and later remove OldBooks if everything is OK).

Can be also used to add individual files, for example:

    calibre_add_if_missing *.pdf *.djvu subdir/*.pdf

There are also some useful options, run --help to see them.

"""
from __future__ import print_function

import shutil
import re
import os.path
from collections import defaultdict
from mekk.calibre.calibre_util import \
    find_calibre_file_names, add_to_calibre
from mekk.calibre.disk_util import \
    find_disk_files, file_size, are_files_equivalent
# TODO: migrate to argparse some day
from optparse import OptionParser


def process_options():
    usage = "Usage: %prog [options] file-or-dir-1 file-or-dir-2 ..."
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--dry-run",
                      action="store_true", default=False, dest="dry_run",
                      help="Do not add anything (and do not move files), just print what I would do.")
    parser.add_option("-c", "--cache",
                      action="store_true", default=False, dest="cache",
                      help="Use cached calibre catalog from previous run to speed up things.")
    parser.add_option("-x", "--tag",
                      action="store", type="string", dest="tag",
                      help="Tag added files with given tag(s). Value can be comma-separated.")
    parser.add_option("-l", "--language",
                      action="store", type="string", dest="language",
                      help="Language(s) to specify for imported book(s). Can be comma-separated.")
    parser.add_option("-a", "--author",
                      action="store", type="string", dest="author",
                      help="Force given author name.")
    parser.add_option("-m", "--move",
                      action="store", type="string", dest="move",
                      help="Move source files to given directory after adding them")
    parser.add_option("-n", "--title-from-name",
                      action="store_true", default=False, dest="title_from_name",
                      help="Always use file name as book title (by default we use file name for doc/rtf/txt, but embedded matadata for pdf, epub, mobi and other formats).")
    (options, args) = parser.parse_args()
    if not args:
        parser.error("""No file or directory specified. Execute with:
    calibre_add_if_missing  /some/dire/ctory/name"
or
    calibre_add_if_missing  file.name otherfile.name dir.name
""")
    if options.move:
        if not os.path.isdir(options.move):
            parser.error("Parameter given for --move ('%s') is not a directory!" % options.move)
    return (options, args)


class KnownFiles(object):
    """
    Registry of all files already known, and possible duplicate checker.
    """

    # Note: we select possible duplicate candidates by size (which
    # makes best filter), but use rounded size because in some cases
    # slightly different files can be equivalent (for example .epub
    # with added bookmarks or slightly changed compression)

    # How big difference can still mean equivalent file
    SIZE_ROUNDING = 1024  # 1kB, dodanie bookmarksów zwykle dorzuca 200-400 bajtów

    def __init__(self):
        # Maps rounded file size to actual disk filename:
        #   size/SIZE_ROUNDING (both floor and ceil) -> set of files with that size
        self.size_to_name = defaultdict(lambda: set())
        self.known_missing = set()

    def load_from_calibre(self, use_cache=False, limit_to_search=None):
        """Loads all calibre files or all files matching given search criteria"""
        for file_name in find_calibre_file_names(use_cache=use_cache, search=limit_to_search):
            self.register_known_file(file_name)

    def register_known_file(self, file_name):
        try:
            chunk = file_size(file_name) // self.SIZE_ROUNDING
            self.size_to_name[chunk].add(file_name)
            self.size_to_name[chunk + 1].add(file_name)
        except OSError as e:
            # print("File {0} does not exist or can't be read, skipping from analysis.\n    Error details: {1}".format(file_name, str(e)))
            if file_name not in self.known_missing:
                print("Skipping missing or inaccessible file: {0}".format(file_name, str(e)))
            else:
                self.known_missing.add(file_name)

    def look_for_the_file(self, file_name):
        """Checks whether the file is already known. Returns the name, if so, or None, if not"""
        chunk = file_size(file_name) // self.SIZE_ROUNDING
        candidates = self.size_to_name[chunk].union(self.size_to_name[chunk + 1]).union(self.size_to_name[chunk - 1])
        # print("Checking {0} (base chunk {1}) against {2}".format(file_name, chunk, ", ".join(candidates)))
        for c in candidates:
            try:
                if are_files_equivalent(file_name, c):
                    return c
            except Exception as err:
                print("""Error while comparing files, assuming files are different.
    checked: {0}
    library: {1}
    details: {2}
""".format(file_name, c, str(err)))
        return None


def move_file(file_name, move_target):
    """Moves file out to directory move_target, supporting renames in case of conflicts"""
    # This fails if such file already exists
    #   shutil.move(file_name, options.move)
    # ... so let's calculate new name if necessary
    base_name = os.path.basename(file_name)
    dest_path = os.path.join(move_target, base_name)
    idx = 0
    while os.path.exists(dest_path):
        idx += 1
        dest_dir = os.path.join(move_target, "sub_" + str(idx))
        dest_path = os.path.join(dest_dir, base_name)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
    shutil.move(file_name, dest_path)


def file_name_and_extension(file_name):
    """Calculates bare file name, and file extension"""
    base_file_name = os.path.basename(file_name)
    m = re.match("^(.*)\.([a-z]+)$", base_file_name)
    if m:
        return m.group(1), m.group(2)
    else:
        return base_file_name, ''


def forced_title(file_name, options):
    """Makes final decision whether title should be enforced. Returns enforced title or None."""
    # doc, rtf and txt files are notoriously bad at metadata extraction, better
    # force filename into the title to know what is the book about.
    # TODO: make this behaviour an option
    bare_name, extension = file_name_and_extension(file_name)
    if options.title_from_name or (extension in ['txt', 'doc', 'docx', 'rtf']):
        return bare_name
    else:
        return None


def run():
    """
    Run calibre_add_if_missing script
    """
    options, args = process_options()

    print("Calculating files to add")

    files_to_check = []
    for param in args:
        if os.path.isdir(param):
            files_to_check.extend(find_disk_files(param))
        else:
            files_to_check.append(param)

    known_files = KnownFiles()

    # Deduplicate imported files, dupes may happen here too
    # TODO

    print("Loading calibre database contents")
    known_files.load_from_calibre(use_cache=options.cache)
    # In case we use cache, let's recheck fresh additions nevertheless (for reruns)
    if options.cache:
        known_files.load_from_calibre(limit_to_search="date:>=today")

    print("Checking and importing books")

    added_count = 0
    skipped_count = 0
    for file_name in files_to_check:
        existing_dupe = known_files.look_for_the_file(file_name)

        if existing_dupe:
            print("Already present: %s (stored as %s)" % (file_name, existing_dupe))
            skipped_count += 1
        else:
            print("Not registered by calibre, adding:", file_name)
            if options.dry_run:
                continue
            book_id = add_to_calibre(
                file_name,
                force_title=forced_title(file_name, options),
                force_tags=options.tag,
                force_author=options.author,
                force_language=options.language)
            # Adding new file to known database.
            if book_id:
                known_files.load_from_calibre(limit_to_search="id:={0}".format(book_id))
            else:
                known_files.load_from_calibre(limit_to_search='date:>=today')   # Best guess
            added_count += 1

        if options.move:
            if not options.dry_run:  # we should not be here but better be safe than sorry
                move_file(file_name, options.move)

    print()
    print("%d files already present, %d added" % (skipped_count, added_count))
