##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import print_function

import sys
import os
from os.path import join, dirname, isdir, normpath
from email import message_from_string

import shutil
import zc.recipe.egg
import zc.buildout.easy_install
import pkg_resources

try:
    from urllib2 import urlopen
except ImportError:
    # Py3 location changed.
    from urllib.request import urlopen

logger = __import__('logging').getLogger(__name__)

confPyTemplate = """
templates_path = ['%(templatesDir)s']
source_suffix = '.rst'
master_doc = '%(indexDoc)s'
project = '%(project)s'
copyright = '%(copyright)s'
version = '%(version)s'
release = '%(release)s'
today_fmt = '%%B %%d, %%Y'
pygments_style = 'sphinx'
%(html_style)s
html_static_path = ['%(staticDir)s']
html_last_updated_fmt = '%%b %%d, %%Y'
extensions = %(extensions)r
%(extra_conf)s
"""

class ZopeOrgSetup(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        options['script'] = join(buildout['buildout']['bin-directory'],
                                 options.get('script', self.name))
        self.egg = zc.recipe.egg.Egg(self.buildout, self.name, self.options)
        self._projectsData = {}

    def openfile(self, fn):
        try:
            return open(fn)
        except IOError:
            return urlopen(fn)

    def _copy_static_file(self, installed, partDir, dirName, fileName):
        destDir = join(partDir, dirName)

        if not isdir(destDir):
            os.mkdir(destDir)
        installed.append(destDir)

        usingFile = False

        if fileName not in self.options:
            recipeDir = dirname(__file__)
            shutil.copy(join(recipeDir, fileName),
                        join(destDir, fileName))
            installed.append(join(destDir, fileName))
            usingFile = True
        elif self.options[fileName]:
            with self.openfile(self.options[fileName]) as f:
                with open(join(destDir, fileName), 'w') as w:
                    w.write(f.read())
            installed.append(join(destDir, fileName))
            usingFile = True
        return destDir, usingFile


    def install(self):
        installed = []
        eggs, workingSet = self.egg.working_set()
        if 'doc-eggs' in self.options:
            eggs = self.options['doc-eggs'].split()
        docs = [(workingSet.find(pkg_resources.Requirement.parse(spec)), spec)
                for spec in eggs]

        # Create parts directory for configuration files.
        installDir = join(
            self.buildout['buildout']['parts-directory'], self.name)
        if not isdir(installDir):
            os.mkdir(installDir)

        srcDirs = eval(self.options.get('src-dirs','{}'))

        projectsData = {}
        # Preserve projectsData for testing
        self._projectsData = projectsData
        # for each egg listed as a buildout option, create a configuration space.
        for doc, egg_name in docs:
            if not doc:
                logger.warning("Specified egg '%s' cannot be resolved, ignoring.", egg_name)
                continue

            partDir = join(installDir, doc.project_name)
            if not isdir(partDir):
                os.mkdir(partDir)
            installed.append(partDir)

            # create static directory
            staticDir, usingDefaultCss = self._copy_static_file(
                installed, partDir,
                '.static', 'default.css')

            # create templates directory
            templatesDir, _ = self._copy_static_file(
                installed, partDir,
                '.templates', 'layout.html')

            metadata = dict(message_from_string('\n'.join(
                doc._get_metadata('PKG-INFO'))).items())

            # create conf.py
            confPyPath = join(partDir, 'conf.py')
            with open(confPyPath, 'w') as confPy:
                confPy.write(confPyTemplate % dict(
                    project=metadata.get('Name', doc.project_name),
                    copyright=metadata.get('Author', 'Zope Community'),
                    version=metadata.get('Version', doc.version),
                    release=metadata.get('Version', doc.version),
                    staticDir=staticDir,
                    templatesDir=templatesDir,
                    html_style=("html_style = 'default.css'"
                                if usingDefaultCss
                                else ''),
                    indexDoc=self.options.get('index-doc','index'),
                    extensions=self.options.get('extensions','').split(),
                    extra_conf=self.options.get('extra-conf', ''),
                    )
                )

            installed.append(confPyPath)

            buildDir = self.options.get('build-dir',
                                        join(partDir, 'build'))
            if not isdir(buildDir):
                os.mkdir(buildDir)

            buildDir = os.path.join(buildDir, doc.project_name)
            if not isdir(buildDir):
                os.mkdir(buildDir)

            srcDir = join(doc.location, srcDirs.get(doc.project_name,
                self.options.get('src-dir', doc.project_name.replace('.','/'))))
            # fix bad path on windows (e.g. //foo\bar)
            srcDir = normpath(srcDir)

            projectsData[doc.project_name] = ['-q','-c', partDir,
                                              srcDir, buildDir]

        installed.extend(zc.buildout.easy_install.scripts(
            [(self.options['script'],
              'z3c.recipe.sphinxdoc',
              'main'),
            ],
            workingSet,
            self.options['executable'],
            self.buildout['buildout']['bin-directory'],
            extra_paths=self.egg.extra_paths,
            arguments = "%r" % projectsData,
        ))

        return installed

    update = install


def main(projects, argv=None, exit_on_error=False):
    import sphinx
    argv = argv or sys.argv
    for project, args in projects.items():
        print("building docs for", project, "---> sphinx-build", " ".join(args))
        code = sphinx.build_main(argv=argv+args)
        if exit_on_error and code:
            sys.exit(code) # pragma: no cover
