# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2017-05-06 23:13:12
# @Last Modified by:   Administrator
# @Last Modified time: 2017-05-16 11:21:03

'''
Command-line interface for the CAAS API.
'''

import argparse
import logging
import os
import sys

import six

from caasclient import client as caas_client
from caasclient.v1 import shell as caas_shell

class CaasClientArgumentParser(argparse.ArgumentParser):

	def __init__(self, *args, **kwargs):
		super(CaasClientArgumentParser, self).__init__(*args, **kwargs)

class CaasShell(object):
	def get_base_parser(self):
		parser = CaasClientArgumentParser(
			prog = 'caas',
			description= 'description',
			epilog = 'See "caas help COMMAND" '
					  'for help on a specific command.',
			add_help = True,
			#formatter_class = 
		)

		parser.add_argument('-v', '--version',
							action='version',
							version='%(prog)s 1.0')

		# parser.add_argument('-h', '--help',
		# 					action='store_true')

		return parser

	def get_subcommand_parser(self):
		parser = self.get_base_parser()

		self.subcommands = {}
		subparsers = parser.add_subparsers(metavar='<subcommand>')

		# actions_modules = caas_shell
		actions_module = caas_shell

		# for actions_module in actions_modules:
		self._find_actions(subparsers, actions_module)
		self._find_actions(subparsers, self)

		return parser

	def _find_actions(self, subparsers, actions_module):
		for attr in (a for a in dir(actions_module) if a.startswith('do_')):
			subcommand = attr[3:].replace('_', '-')
			callback = getattr(actions_module, attr)
			arguments = getattr(callback, 'arguments', [])

			subparser = (
				subparsers.add_parser(subcommand)
			)
			# subparser.add_argument('-h', '--help',
			# 						action='store_true')

			self.subcommands[subcommand] = subparser
			for (args,kwargs) in arguments:
				subparser.add_argument(*args,**kwargs)	
			subparser.set_defaults(func=callback)


	def main(self, argv):
		# Compatible Python 3.4
		argv = list(argv)

		# Parse args once partially to find version and construct subcommands
		# parser = self.get_base_parser()
		# (options, args) = parser.parse_known_args(argv)

		subcommand_parser = (
			self.get_subcommand_parser()
			#self.get_subcommand_parser(options.api_version)
		)

		self.parser = subcommand_parser

		args = subcommand_parser.parse_args(argv)

		self.client = caas_client.Client(caas_url='localhost:5000')

		args.func(self.client, args)

def main():
	try:
		CaasShell().main(sys.argv[1:])
	except Exception as e:
		# TODO: Raise Exceptions
		raise e
		sys.exit(1)

if __name__ == "__main__":
	main()