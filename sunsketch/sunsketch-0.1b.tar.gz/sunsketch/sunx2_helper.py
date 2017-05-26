import tkinter as tk
import sys , os


def returnsize(size):
	if size == "small":
		return [400,400]
	elif size == "medium":
		return [600,600]
	elif size == "huge":
		return [800,800]
	elif size == "smaller":
		return [250,250]
	elif size == "compat":
		return [100,100]
	elif size == "device":
		return [250,300]
	else:
		return [int(size.split('x')[0]),int(size.split('x')[1])]



class Show(object):
	def __init__(self,master,size="device",color='white',title="Showcase"):
		self.master = master
		self.color=color
		master.minsize(returnsize(size)[0],returnsize(size)[1])
		master.configure(background=color)
		master.title(title)
	def add(self,text,padding=10,color='default',weight='normal',font=10,font_color='black'):
		col = self.color if color=="default" else color
		label = tk.Label(self.master,fg=font_color,text=text,pady=padding,bg=col,font="-size {0} -weight {1}".format(font,weight))
		label.pack()
