#AUTH
'''
   Sun Softwares Module v1 
   Module to display objects.

'''
import sys
sys.path.append('/path/to/sunsketch')
#imports
import tkinter as tk
import os
from sunsketch import sunx2_helper as sh






def draw(put ,title="Display" , size="device" , font_bg="white" , font=20 , weight="normal" , color = ['white','black']):
	'''
	Displays a result 
	uses Display('str' , title="display" ) 
	supported args title ( window title ) , size (small , medium, compat , smaller , device , huge or 120x233 format) , weight = bold , italic , normal , color = [windowcolor , textcolor] , font = font size
	
	'''
	window = tk.Tk()
	window.configure(background=color[0])
	window.title(title)
	try:
		size=sh.returnsize(size)
	except:
		print("Size is error")
		return
	window.minsize(size[0],size[1])
	l1 = tk.Label(window,text=put,fg=color[1] , bg = font_bg , font='-size {0} -weight {1}'.format(font,weight))
	l1.pack() 
	window.mainloop()

ob , fonts , weights , paddings , colors, font_colors = [] , [] , [] , [] , [] , []


def add(item,color="default",font=10,padding=10,weight='normal',font_color='black'):
	global ob
	global fonts
	global paddings
	global weights
	global colors
	global font_colors

	ob = ob + [item]
	colors = colors + [color]
	fonts = fonts + [font]
	paddings = paddings +  [padding]
	weights = weights + [weight]
	font_colors = font_colors + [font_color]
def show(title="Showcase",size="device",color="white"):
	root = tk.Tk()
	gui = sh.Show(root,size=size,color=color,title=title)
	for item in ob:
		posi = ob.index(item)
		gui.add(item,padding=paddings[posi],color=colors[posi],weight=weights[posi],font=fonts[posi],font_color=font_colors[posi])
	root.mainloop()
		
		


if __name__=="__main__":
	print('A Graphics display script created by sun')


	
	
	
	
	
	
	
	
	
	



