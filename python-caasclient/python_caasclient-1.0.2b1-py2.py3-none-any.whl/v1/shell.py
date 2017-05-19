# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2017-05-16 10:38:02
# @Last Modified by:   Administrator
# @Last Modified time: 2017-05-16 11:23:39

# Framework Completed
# !Commands add on demand

import argparse
from caasclient import utils

@utils.arg('--name',
			metavar='<name>',
			required=True,
			help="Name of the project to create.")
def do_test(cli, args):
	print args

@utils.arg('--name')
def do_project_create(cli, args):
	print args
	try:
		project = cli.project.create(args)
		print("Request to create cluster %s has been accepted." % str(project.id))
	except Exception as e:
		print("Create for project %s failed: %s" %
				(args.name, e))

@utils.arg('project',
			metavar='<project>',
			nargs='+',
			help='')
def do_project_delete(cli, args):
	pass