#!/usr/bin/env python3
import os
import sys

if __name__ == '__main__':
	os.environ.setdefault('PYPLANET_SETTINGS_MODULE', 'settings')
	try:
		from pyplanet.core.management import execute_from_command_line
	except ImportError as exc:
		raise ImportError(
			'Couldn\'t import PyPlanet. Are you sure it\'s installed and '
			'available on your PYTHONPATH environment variable? Did you '
			'forget to activate a virtual environment?'
		) from exc
	execute_from_command_line(sys.argv)
