# -*- coding: UTF-8 -*-
# !/usr/bin/env python

import click
import os, random, sys
import codecs
from colors import red, yellow

currentPath = os.getcwd()
BLOCKSIZE = 1048576

@click.command()
@click.argument('file')
@click.argument('name', nargs=-1)



def entry(file, name):
    '''
    cover ANSI to utf8

    a2u filename [OPTION]
    '''

    if not os.path.exists(file):
        click.echo(red('a2u: No such file or directory'))
        sys.exit(0)

    sourceFileName = file
    targetFileName = name and name[0] or os.path.join(currentPath, os.path.basename(file))

    if os.path.exists(targetFileName):

        yn = raw_input(yellow('Whether to replace the same name file? [y/N]: '))

        if yn is not 'y':
            splitext = os.path.splitext(os.path.basename(file))
            targetFileName = os.path.join(currentPath, splitext[0] + str(random.randint(100000, 999999)) + splitext[1])

    with codecs.open(sourceFileName, "r", "gbk") as sourceFile:
        with codecs.open(targetFileName, "w", "utf-8") as targetFile:
            while True:
                contents = sourceFile.read(BLOCKSIZE)
                if not contents:
                    break
                targetFile.write(contents)