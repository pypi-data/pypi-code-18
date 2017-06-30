#!/usr/bin/env python3


#This script deals with optimizations.
#
#copyright (C) 2017  Martin Engqvist | martin_engqvist@hotmail.com
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#LICENSE:
#
#This script is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#
#This script is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Library General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software Foundation,
#Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



import algorithms
import bezier
import convert





# def scale(col1, col2, number=100, mode='rgb', white_mid=False):
# 	'''
# 	Function makes a color scale from 0 to 100 using the supplied colors.
# 	The variable white_mid is boolean and determines whether the colors
# 	should transition over white in the middle or just smoothly run into each other.
# 	The function returns a dictionary of integer keys and hex color values corresponding to the scores 0 to 100.
# 	'''
# 	col1 = convert.Color(col1) # convert first color to a color object
# 	col1 = convert.Color(col2) # convert second color to a color object
# 	assert type(white_mid) is bool, 'Error, white_mid must be a boolean.'
#
# 	color_dict={}
# 	if white_mid is False:
# 		#determine how many points R, G and B should change with each score
# 		R_diff = (col2.rgb()[0]-col1.rgb()[0])/100.0
# 		G_diff = (col2.rgb()[1]-col1.rgb()[1])/100.0
# 		B_diff = (col2.rgb()[2]-col1.rgb()[2])/100.0
#
# 		#set starting values
# 		R, G, B = col1.rgb()
# 		for i in range(number+1):
# 			color_dict[i] = convert.Color( (R+int(R_diff*i), G+int(G_diff*i), B+int(B_diff*i)) )
#
# 	elif white_mid is True:
# 		first_half = scale((col1), (255,255,255))
# 		for key in range(0, number, 2):
# 			color_dict[key/2] = first_half[key]
#
# 		second_half = scale((255,255,255), col2)
# 		for key in range(0, number+2, 2):
# 			color_dict[50+key/2] = second_half[key]
#
# 	return color_dict



def rainbow(start_col, end_col=False, number=10, clockwise=True):
	'''
	Returns the entire color wheel starting with the input color.
	number specifies how many new ones to return.
	'''
	start_col = convert.Color(start_col) # convert input color to a color object
	assert type(number) is int, 'Error, the input number must be an integer.'
	assert (2 <= number and number <= 1000), 'Error, the input number must be between 2 and 1000'


	#assign to  variables
	r, g, b = start_col.rgb()

	# Convert to [0, 1]
	r, g, b = [x/255. for x in [r, g, b]]

	# RGB -> HLS
	hue, lightness, saturation = convert.colorsys.rgb_to_hls(r, g, b)

	# Rotation by defined number of degrees
	angle = (360/float(number))/360.0

	if clockwise is False:
            h_list = [(hue+ang) % 1 for ang in [angle*s for s in range(number)]]

	elif clockwise is True:
		h_list = [(hue+ang) % 1 for ang in [-angle*s for s in range(number)]]

	else:
		raise ValueError

	colors = [[int(round(x*255)) for x in convert.colorsys.hls_to_rgb(h, lightness, saturation)] for h in h_list] # HLS -> new RGB
	colors = [tuple(s) for s in colors]

	#if the input was hex, convert it back
	if start_col.get_format == 'hex':
		colors = [rgb_to_hex(s) for s in colors]

	#return as color objects
	return [convert.Color(s) for s in colors]



def _linear_bez(colors, step_num):
    '''
    Helper function to calculate linear bezier from two colors.
    '''
    color1, color2 = colors
    col1_hsl = color1.hsl()
    col2_hsl = color2.hsl()

    assert col1_hsl[2] != col2_hsl[2], 'Error, the two colors must differ in lightness.'

    #figure out how much lightness should change if evenly stepped
    stepsize = (col2_hsl[2]-col1_hsl[2])/(float(step_num)-1.0)
    steps = [col1_hsl[2] + stepsize * s for s in range(step_num)]
    #print('steps', steps)

    #find out which bezier t-values corresponds to these lightness steps
    if col1_hsl[2] <= col2_hsl[2]: #darkest color is first
        min_hsl = float(col1_hsl[2])
        max_hsl = float(col2_hsl[2])
        t_values = [algorithms.divide_and_conquer(0.0, 1.0, data=[min_hsl, max_hsl], target=s, func=bezier.calculate_linear_bezier) for s in steps]

    elif col1_hsl[2] > col2_hsl[2]: #lightest color is first
        min_hsl = float(col2_hsl[2])
        max_hsl = float(col1_hsl[2])
        t_values = [algorithms.divide_and_conquer(0.0, 1.0, data=[min_hsl, max_hsl], target=s, func=bezier.calculate_linear_bezier) for s in steps]
        t_values = t_values[::-1]


    #now get the colors for these steps
    h_vals = [bezier.calculate_linear_bezier([col1_hsl[0], col2_hsl[0]], t) for t in t_values]
    s_vals = [bezier.calculate_linear_bezier([col1_hsl[1], col2_hsl[1]], t) for t in t_values]
    l_vals = [bezier.calculate_linear_bezier([col1_hsl[2], col2_hsl[2]], t) for t in t_values]

    #combine h, s and l components
    hsl_cols = list(zip(h_vals, s_vals, l_vals))

    return [convert.Color(convert.hsl_to_hex(s)) for s in hsl_cols]



def _quadratic_bez(colors, step_num):
	'''
	Helper function to calculate quadratic bezier from three colors.
	'''
	color1, color2, color3 = colors
	col1_hsl = color1.hsl()
	col2_hsl = color2.hsl()
	col3_hsl = color3.hsl()

	assert col1_hsl[2] != col3_hsl[2], 'Error, the first and last color must differ in lightness.'

	#adjust lightness of middle color
	if col1_hsl[2] > col3_hsl[2]:
		color2 = color2.set_l( col1_hsl[2] - (col1_hsl[2]-col3_hsl[2])/2 )
		col2_hsl = color2.hsl()
	else:
		color2 = color2.set_l( col3_hsl[2] - (col3_hsl[2]-col1_hsl[2])/2 )
		col2_hsl = color2.hsl()

	#figure out how much lightness should change if evenly stepped
	stepsize = (col3_hsl[2]-col1_hsl[2])/(float(step_num)-1.0)
	steps = [col1_hsl[2] + stepsize * s for s in range(step_num)]
	#print(steps)

	#find out which bezier t-values corresponds to these lightness steps
	if col1_hsl[2] <= col2_hsl[2] <= col3_hsl[2]: #darkest color is first
		min_hsl = float(col1_hsl[2])
		med_hsl = float(col2_hsl[2])
		max_hsl = float(col3_hsl[2])
		t_values = [algorithms.divide_and_conquer(0.0, 1.0, data=[min_hsl, med_hsl, max_hsl], target=s, func=bezier.calculate_quadratic_bezier) for s in steps]

	elif col1_hsl[2] >= col2_hsl[2] >= col3_hsl[2]: #lightest color is first
		min_hsl = float(col3_hsl[2])
		med_hsl = float(col2_hsl[2])
		max_hsl = float(col1_hsl[2])
		t_values = [algorithms.divide_and_conquer(0.0, 1.0, data=[min_hsl, med_hsl, max_hsl], target=s, func=bezier.calculate_quadratic_bezier) for s in steps]
		t_values = t_values[::-1]

	else:
		raise ValueError

	#now get the colors for these steps
	h_vals = [bezier.calculate_quadratic_bezier([col1_hsl[0], col2_hsl[0], col3_hsl[0]], t) for t in t_values]
	s_vals = [bezier.calculate_quadratic_bezier([col1_hsl[1], col2_hsl[1], col3_hsl[1]], t) for t in t_values]
	l_vals = [bezier.calculate_quadratic_bezier([col1_hsl[2], col2_hsl[2], col3_hsl[2]], t) for t in t_values]

	#combine h, s and l components
	hsl_cols = list(zip(h_vals, s_vals, l_vals))
	return [convert.Color(convert.hsl_to_hex(s)) for s in hsl_cols]



def _cubic_bez(colors, step_num):
	'''
	Helper function to calculate cubic bezier from four colors.
	'''
	color1, color2, color3, color4 = colors
	col1_hsl = color1.hsl()
	col2_hsl = color2.hsl()
	col3_hsl = color3.hsl()
	col4_hsl = color4.hsl()

	assert col1_hsl[2] != col4_hsl[2], 'Error, the first and last color must differ in lightness.'

	#adjust lightness of middle color
	if col1_hsl[2] > col4_hsl[2]:
		color2 = color2.set_l( col1_hsl[2] - (col1_hsl[2]-col4_hsl[2])/3 )
		color3 = color3.set_l( col1_hsl[2] - 2*(col1_hsl[2]-col4_hsl[2])/3 )
		col2_hsl = color2.hsl()
		col3_hsl = color3.hsl()
		print(col1_hsl[2], col2_hsl[2], col3_hsl[2], col4_hsl[2])
	else:
		color2 = color2.set_l( col4_hsl[2] - 2*(col4_hsl[2]-col1_hsl[2])/3 )
		color3 = color3.set_l( col4_hsl[2] - (col4_hsl[2]-col1_hsl[2])/3 )
		col2_hsl = color2.hsl()
		col3_hsl = color3.hsl()
		print(col1_hsl[2], col2_hsl[2], col3_hsl[2], col4_hsl[2])

	#figure out how much lightness should change if evenly stepped
	stepsize = (col4_hsl[2]-col1_hsl[2])/(float(step_num)-1.0)
	steps = [col1_hsl[2] + stepsize * s for s in range(step_num)]
	#print(steps)

	#find out which bezier t-values corresponds to these lightness steps
	if col1_hsl[2] <= col2_hsl[2] <= col3_hsl[2]: #darkest color is first
		min_hsl = float(col1_hsl[2])
		med1_hsl = float(col2_hsl[2])
		med2_hsl = float(col3_hsl[2])
		max_hsl = float(col4_hsl[2])
		t_values = [algorithms.divide_and_conquer(0.0, 1.0, data=[min_hsl, med1_hsl, med2_hsl, max_hsl], target=s, func=bezier.calculate_cubic_bezier) for s in steps]

	elif col1_hsl[2] >= col2_hsl[2] >= col3_hsl[2]: #lightest color is first
		min_hsl = float(col4_hsl[2])
		med1_hsl = float(col3_hsl[2])
		med2_hsl = float(col2_hsl[2])
		max_hsl = float(col1_hsl[2])
		t_values = [algorithms.divide_and_conquer(0.0, 1.0, data=[min_hsl, med1_hsl, med2_hsl, max_hsl], target=s, func=bezier.calculate_cubic_bezier) for s in steps]
		t_values = t_values[::-1]
	else:
		raise ValueError

	#now get the colors for these steps
	h_vals = [bezier.calculate_cubic_bezier([col1_hsl[0], col2_hsl[0], col3_hsl[0], col4_hsl[0]], t) for t in t_values]
	s_vals = [bezier.calculate_cubic_bezier([col1_hsl[1], col2_hsl[1], col3_hsl[1], col4_hsl[1]], t) for t in t_values]
	l_vals = [bezier.calculate_cubic_bezier([col1_hsl[2], col2_hsl[2], col3_hsl[2], col4_hsl[2]], t) for t in t_values]

	#combine h, s and l components
	hsl_cols = list(zip(h_vals, s_vals, l_vals))
	return [convert.Color(convert.hsl_to_hex(s)) for s in hsl_cols]



def sequential(colors, step_num):
    '''
    Create a sequential color scale going from a starting color to white or light yellow
    color is the starting color in hex
    end is either "white" or "yellow"

    The function will use bezier smoothing to avoid harsh color transitions.
    Furthermore, it will even out the lightness profile so that it is linear.
	This ensures good color scales.
    '''
    assert 2 <= len(colors) <= 4, 'Error, supply between two and four colors for a sequential scale.'
    #assert that the colors are valid
	#they must also be continually lighter or continually darker

    colors = [convert.Color(s) for s in colors] #convert to color objects

    if len(colors) == 2: # linear bezier interpolation
        return _linear_bez(colors, step_num)

    elif len(colors) == 3: # quadratic bezier interpolation
        return _quadratic_bez(colors, step_num)

    elif len(colors) == 4: # cubic bezier interpolation
        return _cubic_bez(colors, step_num)



def diverging(colors, step_num):
	'''
	Generates a color scale that can be used for visualizing data.
	colors should be a list of colors which a are used for creating the scale
	number defines how many colors should get returned
	'''
	#there should be 3 or 5 colors where the center one is the middle color of the scale
	#assert len(colors) == 3 or len(colors) == 5, 'Error, please supply three or five colors where the centre one is your midpoint color.'

	colors = [convert.Color(s) for s in colors] #convert to color objects

	# if 2 or 4, automatically chooose white as mid color..... ###
	if len(colors) == 2:
		colors.insert(1, convert.Color('#ffffff'))
		print('You supplied an even number of colors, inserting white as midpoint in the diverging scale.')
	elif len(colors) == 4:
		colors.insert(2, convert.Color('#ffffff'))
		print('You supplied an even number of colors, inserting white as midpoint in the diverging scale.')

    #adjust the lightness of the two extreme colors such that they match
	h1, s1, l1 = colors[0].hsl()
	h2, s2, l2 = colors[-1].hsl()
	if l1 > l2:
		colors[0] = colors[0].set_l(l2)
	elif l1 < l2:
		colors[-1] = colors[-1].set_l(l1)
	elif l1 == l2:
		pass
	else:
		raise ValueError

    #if 3 colors, do linear interpolation and lightness correction. Operate on each half by itself and then add together.
	if len(colors) == 3:
		left_part = _linear_bez(colors[:2], int(step_num//2+1))
		right_part = _linear_bez(colors[1:], int(step_num//2+1))
		return left_part[:-1] + right_part

    #if 5 colors, do quadratic bezier interpolation and lightness correction. Operate on each half by itself and then add together.
	if len(colors) == 5:
		left_part = _quadratic_bez(colors[0:3], int(step_num/2+1))
		right_part = _quadratic_bez(colors[2:], int(step_num/2+1))
		return left_part[:-1] + right_part



def diverging_preset(scale, number=10):
	'''
	Use preset colors to generate diverging scales.
	'''
	pass
	#good scales

	#purple to teal
	#col1 = '#800080'
	#col2 = '#008080'

	#orange to blue
	#col1 = '#ffc500'
	#col2 = '#056efa'

	#blue to red
	#col1 = '#817cbb'
	#col2 = '#c12133'

	#another blue to red
	#col1 = '#30acdf'
	#col2 = '#ef292b'

	#orange to green
	#col1 = '#ff6600'
	#col2 = '#2c9082'

	#orange to dark blue
	#col1 = '#ff6600'
	#col2 = '#18567d'

	#grey to orange
	#col1 = '#666666'
	#col2 = '#ff6600'

	#dark yellow to blue
	#col1 = '#cba916'
	#col2 = '#8eb6d5'

def qualitative(number, scale=1):
	'''
	Return a list of qualitative colors for plotting categorical data.
	number defines how many (12 is max)
	scale defines which one of three pre-defined scales should be used
	'''
	assert 1 <= number <= 12, 'Error, the number of colors must be between 1 and 12'
	assert 1 <= scale <= 2, 'Error, scale must be between 1 and 2'

	sc1 = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928']
	sc2 = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5', '#d9d9d9', '#bc80bd', '#ccebc5', '#ffed6f']
	sc3 = []
	sc4 = []
	sc5 = []
	sc6 = []
	sc7 = []
	sc8 = []
	sc9 = []
	sc10 = []
	sc11 = []
	sc12 = []
	all_scales = [sc1, sc2, sc3, sc4, sc5, sc6, sc7, sc8, sc9, sc10, sc11, sc12]
	return all_scales[scale-1][:number]



def visualize(colors):
	'''Visualize colors'''
	convert.visualize(colors)

#def binary(scale=1):
#	'''
#	Return
#	'''
#
#	if scale == 1:
#		return

# def mix_colors(col1, col2):
# 	'''
# 	Mix two colors and return the result.
# 	The input colors can be either RGB or hex.
# 	It is also possible to use one RGB value and one hex value.
# 	'''
# 	color_dict = scale(col1, col2, white_mid=False)
# 	return color_dict[50]
