import sys; sys.path.append('../icheckin')
from icheckin import commands, constants
from collections import OrderedDict
from imp import reload
from os.path import exists
import os

def setup_module(module):
	def _a():
		print('A')

	def _b(args):
		print('B')

	def _c(args):
		print('C')

	def _d():
		print('D')

	def _e(args):
		print('E')

	def _f(args):
		print('F')

	commands.commands = OrderedDict()
	commands.commands['-a'] = {
		'alt'	: '--apple',
		'info': 'Apple',
		'action': _a,
		'params': []
	}
	commands.commands['-b'] = {
		'alt': '--boy',
		'info': 'Boy',
		'action': _b,
		'params': ['one']	
	}
	commands.commands['-c'] = {
		'alt': '',
		'info': 'Cat',
		'action': _c,
		'params': ['one one', 'two']	
	}
	commands.commands['-d'] = {
		'alt': '',
		'info': 'Dog',
		'action': _d,
		'params': []	
	}
	commands.commands['-e'] = {
		'alt': '--elephant',
		'info': 'Elephant',
		'action': _e,
		'params': ['one one', 'two', 'three three three']	
	}
	commands.commands['-f'] = {
		'alt': '--fool',
		'info': 'Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool ' + 
			'Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool ' +
			'Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool ' + 
			'Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool ' + 
			'Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool ',
		'action': _f,
		'params': ['one one', 'two', 'three three three']	
	}

	global usageMsg
	usageMsg = '''
usage: icheckin [-a | --apple] [-b | --boy <one>] [-c <one one> <two>] [-d]
                [-e | --elephant <one one> <two> <three three three>]
                [-f | --fool <one one> <two> <three three three>]
'''.strip('\n')
	global detailsMsg
	detailsMsg = '''
   -a, --apple      Apple
   -b, --boy        Boy
   -c               Cat
   -d               Dog
   -e, --elephant   Elephant
   -f, --fool       Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool
                    Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool
                    Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool
                    Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool
                    Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool Fool
                    Fool Fool Fool Fool
'''.strip('\n')
	global parametersMsg
	parametersMsg = '''
error: invalid parameters
'''.strip('\n')
	global commandMsgA
	commandMsgA = '''
command: icheckin -a
'''.strip('\n')
	global commandMsgB
	commandMsgB = '''
command: icheckin -b <one>
'''.strip('\n')
	global commandMsgF
	commandMsgF = '''
command: icheckin -f <one one> <two> <three three three>
'''.strip('\n')
	global unknownMsgZ
	unknownMsgZ = '''
unknown command: -z
'''.strip('\n')
	global unknownMsgFool
	unknownMsgFool = '''
unknown command: -fool
'''.strip('\n')
	global credentials
	credentials = '''
%s
123

%s
456
''' % (constants.KEYWORD_1, constants.KEYWORD_2)
	credentials = credentials.strip('\n')

def test_process_valid_command_no_parameter(capfd):
	assert commands.process(['-a']) == True
	out, err = capfd.readouterr()
	assert out == 'A' + '\n'
	assert commands.process(['--apple']) == True
	out, err = capfd.readouterr()
	assert out == 'A' + '\n'
	assert commands.process(['-d']) == True
	out, err = capfd.readouterr()
	assert out == 'D' + '\n'

def test_process_valid_command_valid_parameters(capfd):
	assert commands.process(['-b', '1']) == True
	out, err = capfd.readouterr()
	assert out == 'B' + '\n'
	assert commands.process(['--boy', '1']) == True
	out, err = capfd.readouterr()
	assert out == 'B' + '\n'
	assert commands.process(['-c', '1', '2']) == True
	out, err = capfd.readouterr()
	assert out == 'C' + '\n'
	assert commands.process(['-e', '1', '2', '3']) == True
	out, err = capfd.readouterr()
	assert out == 'E' + '\n'
	assert commands.process(['--elephant', '1', '2', '3']) == True
	out, err = capfd.readouterr()
	assert out == 'E' + '\n'
	assert commands.process(['-f', '1', '2', '3']) == True
	out, err = capfd.readouterr()
	assert out == 'F' + '\n'
	assert commands.process(['--fool', '1', '2', '3']) == True
	out, err = capfd.readouterr()
	assert out == 'F' + '\n'

def test_process_valid_command_invalid_parameters(capfd):
	assert commands.process(['-a', '1']) == False
	out, err = capfd.readouterr()
	assert out == parametersMsg + '\n' + commandMsgA + '\n'
	assert commands.process(['-b']) == False
	out, err = capfd.readouterr()
	assert out == parametersMsg + '\n' + commandMsgB + '\n'
	assert commands.process(['-f', '1']) == False
	out, err = capfd.readouterr()
	assert out == parametersMsg + '\n' + commandMsgF + '\n'

def test_process_invalid_command_no_parameter(capfd):
	assert commands.process(['-z']) == False
	out, err = capfd.readouterr()
	assert out == unknownMsgZ + '\n' + usageMsg + '\n'
	assert commands.process(['-fool']) == False
	out, err = capfd.readouterr()
	assert out == unknownMsgFool + '\n' + usageMsg + '\n'

def test_process_invalid_command_with_parameters(capfd):
	assert commands.process(['-z', '1' , '2']) == False
	out, err = capfd.readouterr()
	assert out == unknownMsgZ + '\n' + usageMsg + '\n'
	assert commands.process(['-fool', '1' , '2']) == False
	out, err = capfd.readouterr()
	assert out == unknownMsgFool + '\n' + usageMsg + '\n'

def test_display_help(capfd):
	assert commands._usage() == usageMsg
	assert commands._details() == detailsMsg
	commands._help()
	out, err = capfd.readouterr()
	assert out == usageMsg + '\n\n' + detailsMsg + '\n'

def test_save_new_file(capfd):
	reload(commands)
	if exists(constants.TEST_PATH):
		os.remove(constants.TEST_PATH)
	commands._save(['123', '456'], test=True)
	out, err = capfd.readouterr()
	assert out == 'success: credentials saved to %s' % constants.TEST_PATH + '\n'
	with open(constants.TEST_PATH, 'r') as file:
		assert file.readlines() == list(map(lambda x: x+'\n', 
			credentials.split('\n')))

def test_save_overwrite_file(capfd):
	reload(commands)
	with open(constants.TEST_PATH, 'w') as file:
		file.write('000')
	commands._save(['123', '456'], test=True)
	out, err = capfd.readouterr()
	assert out == 'success: credentials saved to %s' % constants.TEST_PATH + '\n'
	with open(constants.TEST_PATH, 'r') as file:
		assert file.readlines() == list(map(lambda x: x+'\n', 
			credentials.split('\n')))

def test_remove_existing_file(capfd):
	reload(commands)
	if not exists(constants.TEST_PATH):
		with open(constants.TEST_PATH, 'w') as file:
			file.write('000')
	commands._remove(test=True)
	out, err = capfd.readouterr()
	assert out == 'success: %s removed' % constants.TEST_PATH + '\n'
	assert exists(constants.TEST_PATH) == False

def test_remove_nonexisting_file(capfd):
	reload(commands)
	if exists(constants.TEST_PATH):
		os.remove(constants.TEST_PATH)	
	commands._remove(test=True)
	out, err = capfd.readouterr()
	assert out == 'error: %s does not exist' % constants.TEST_PATH + '\n'
	assert exists(constants.TEST_PATH) == False

def test_help_action():
	reload(commands)
	assert commands.commands['-h']['action'] == commands._help

def test_save_action():
	reload(commands)
	assert commands.commands['-s']['action'] == commands._save

def test_remove_action():
	reload(commands)
	assert commands.commands['-r']['action'] == commands._remove

def teardown_module(module):
	if exists(constants.TEST_PATH):
		os.remove(constants.TEST_PATH)

