import argparse, yaml, os
from .main import main, HOME, PATH


if __name__ == '__main__':
	args = argparse.ArgumentParser(description='Logfile processing tool')
	args.add_argument('-v', '--version', action='version', version='LogReader ' + str(__version__))
	args.add_argument('-c', dest='config', help='config path')
	args.add_argument('-f', dest='file', help='file path')
	args = args.parse_args()

	if args.config is not None and not os.path.isfile(str(args.config)):
		print('Unavailable path: ' + str(args.config))
	elif os.path.isfile(str(args.config)):
		CONFIGPATH = args.config

		with open(CONFIGPATH) as data:
			print('Config file: ' + CONFIGPATH)
			config = yaml.load(data)
	elif os.path.isfile(HOME + '/.logreader'):
		CONFIGPATH = HOME + '/.logreader'

		with open(CONFIGPATH) as data:
			print('Config file: ' + CONFIGPATH)
			config = yaml.load(data)
	else:
		CONFIGPATH = PATH + '/default.yaml'

		with open(CONFIGPATH) as data:
			print('Default config file: ' + CONFIGPATH)
			config = yaml.load(data)

		if not os.path.isfile(HOME + '/.logreader'):
			print('Create config file: ' + HOME + '/.logreader')
			try:
				with open(HOME + '/.logreader', 'w+') as outfile:
					yaml.dump(config, outfile)
			except Exception:
				pass
	file = None
	if args.file is not None and not os.path.isfile(str(args.file)):
		print('Unavailable path: ' + str(args.file))
		main()
	elif os.path.isfile(str(args.file)):
		print('Input file: ' + str(args.file))
		main(file=str(args.file))
	else:
		main()