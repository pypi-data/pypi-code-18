#!/usr/bin/env python

"""
	pap is a script for generating
	metadata files from git histories
"""

import sys
import subprocess
from packaging import version
from setuptools import find_packages

try:
	from ._version import __version__
except ImportError:
	pass

try:
	from ._author import __author__
except ImportError:
	pass

root_tag = '0.1.0.dev0'
package = find_packages()[0]

def tags(commit='HEAD', filter_func=None):
	process = subprocess.Popen(["git", "tag", "--points-at", commit], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = process.communicate()
	tags = output.decode('utf-8').splitlines()
	if filter is not None:
		tags = list(filter(filter_func, tags))
	return tags

def commit_hash(commit='HEAD'):
	process = subprocess.Popen(["git", "rev-parse", commit], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = process.communicate()
	hash = output.decode('utf-8').splitlines()[0]
	return hash

def is_release(tag):
	return "dev" not in tag

def is_dev(tag):
	return "dev" in tag

def sort(tags):
	versions = []
	for tag in tags:
		versions.append(version.parse(tag))
	return list(map((lambda x: str(x)), sorted(versions)))

def nearest_tag(commit='HEAD', filter_func=None):
	process = subprocess.Popen(["git", "rev-list", commit], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = process.communicate()
	commits = output.decode('utf-8').splitlines()
	index = -1
	for index, commit in enumerate(commits[1:]):
		found_tags = tags(commit, filter_func)
		if not found_tags:
			continue
		return index+1, sort(found_tags)[-1]
	return index+1, root_tag

def get_version(commit):
	"""Given a commit, return a version string"""

	release_tags = tags(commit, is_release)
	dev_tags = tags(commit, is_dev)

	if release_tags:
		return (sort(release_tags)[-1])
	elif dev_tags:
		commits_away, nearest_release = nearest_tag(commit, is_release)
		return ("%s%s+%s" % (sort(dev_tags)[-1][:-1], commits_away, commit[:8]))
	else:
		commits_away, tag = nearest_tag(commit)
		if is_dev(tag):
			commits_away, nearest_release = nearest_tag(commit, is_release)
			return ("%s%s+%s" % (tag[:-1], commits_away, commit[:8]))
		else:
			return ("%s.post.dev%s+%s" % (tag, commits_away, commit[:8]))

def write_version(version, filename=("%s/_version.py" % package)):
	version_docstring = ('"""This document has been generated '
                         'by pap based on the git history"""\n'
                        )
	with open(filename, 'w') as file:
		file.writelines(version_docstring)
		file.write("__version__ = '%s'\n" % (version))

def _f10(seq, idfun=None):
    seen = set()
    if idfun is None:
        for x in seq:
            if x.upper() in map(str.upper, seen):
                continue
            seen.add(x)
            yield x
    else:
        for x in seq:
            x = idfun(x)
            if x in seen:
                continue
            seen.add(x)
            yield x

def f11(seq):
    return list(_f10(seq))

def get_authors():
	process = subprocess.Popen(["git", "log", "--format='%aN <%aE>'"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = process.communicate()
	authors = f11(output.decode('utf-8').splitlines())
	return authors

def write_authors(authors):
	author_docstring = ('"""This document has been generated '
						'by pycompile based on the git history"""\n'
					   )
	author_string = "__author__ = (%s%s\n" % (authors[0][:-1], ", '")
	for author in authors[1:]:
		author_string += "              %s%s\n" % (author[:-1], ", '")
	author_string += "             )\n"

	authors_string = "__authors__ = list(filter(None, [x.strip(' ') for x in __author__.split(',')]))\n"

	with open(package + '/_author.py', 'w') as file:
		file.write(author_docstring)
		file.write(author_string)
		file.write(authors_string)

def main():
	write_authors(get_authors())

	if len(sys.argv) < 2:
		target_commit = commit_hash()
	else:
		target_commit = commit_hash(sys.argv[1])
	write_version(get_version(target_commit))
