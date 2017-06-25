#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  programa.py
#  
#  Copyright 2017 Henrique Brito <henriquebrito54@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

### Function to print list of lists

'''This is nester.py module and provides a mean to print a list of lists recursively using a function called print_lol()'''

#### function ###

def print_lol(the_list):
	
	'''the_list can ba a list of lists# and each argument is printed in one line'''
	
	for each_item in the_list:
		if isinstance(each_item, list): #The BIF insistance(var, type) verifies the kind of variables  that argument receives - returns true or false
			print_lol(each_item)
		else:
			print(each_item)
