#! /usr/bin/env python3
"""(EN) This module replaces the standard sequence data types (lists, tuples, strings) similar types of data,
in which indexation is not from zero but from one. Example: a = humlist(1,2,3); print(a[2]) will print 2.

Contains data types: 
	humlist (similar to lists), humtuple (similar to tuples), humstr (analogue lines)
Contains functions:
	humrange (analogue range)

Importing module: 
1) Add to sys.path to a directory (folder) with this module. 
	Example 1 (simple):
		import sys
		sys.path.append('/home/user/modules')
	Example 2 (with relative paths): 
		import os, sys, inspect
		# realpath() will make your script run, even if you symlink it :)
		cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
		if cmd_folder not in sys.path:
		sys.path.insert(0, cmd_folder)
	Example 3 (with relative paths):
		# use this if you want to include modules from a subfolder
		cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
		if cmd_subfolder not in sys.path:
		sys.path.insert(0, cmd_subfolder)
		You can not add if the module is in the home directory (folder). In some operating systems the home directory is the one in which
		is a file with the executable program.
2) Import: import from humanity *
or: import humanity

(RU) Данный модуль заменяет стандартные типы данных последовательностей (списки, кортежи, строки) аналогичными типами данных,
в которых индексация идет не с нуля а с единицы. Пример: a = humlist(1,2,3); print(a[2]) выведет 2.

Содержит типы данных: 
	humlist (аналог списков), humtuple (аналог кортежей), humstr (аналог строк)
Содержит функции:
	humrange (аналог range)

Подключение модуля: 
1) Добавим в sys.path расположение каталога (папки) с данным модулем. 
	Пример 1 (простой):
		import sys
		sys.path.append('/home/user/modules')
	Пример 2 (с относительными путями): 
		import os, sys, inspect
		# realpath() will make your script run, even if you symlink it :)
		cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
		if cmd_folder not in sys.path:
		sys.path.insert(0, cmd_folder)
	Пример 3 (с относительными путями):
		# use this if you want to include modules from a subfolder
		cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
		if cmd_subfolder not in sys.path:
		sys.path.insert(0, cmd_subfolder)
  Можно не добавлять если данный модуль находится в домашнем каталоге (папке). В некоторых ОС домашний каталог это тот, в котором
  расположен файл с выполняемой программой.
2) Импортируем его: from humanity import *
  или: import humanity

Revision: 8
"""

from .main import *
from .humd import *

__version__ = '3.0.5'


