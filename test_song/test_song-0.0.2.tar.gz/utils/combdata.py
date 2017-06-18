# -*- coding: utf-8 -*-


def re_write_file(source_file, dir_file=None, command=None, func=None, index=1):
	res = ''
	with open(source_file, 'r') as f:
		lines = f.readlines()
		i = 0
		for line in lines:
			if i < index:
				i = i + 1
				continue
			l_list = line.strip().split(',')
			if command:
				res += command
			if func:
				res += func(l_list)
	if dir_file:
		with open(dir_file, "w+") as f:
			f.writelines(res)
	return res
