#!/usr/bin/env python
# -*- coding: ascii -*-
from __future__ import absolute_import
from __future__ import print_function

r"""
A tkinter code that helps users digitize curves from plot images.

If a 2D plot is available only on paper or an image file, but the user needs the x,y data pairs in digital form, DigiPlot will help to create those x,y data pairs.


DigiPlot
Copyright (C) 2017  Charlie Taylor

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

-----------------------

"""
import os
here = os.path.abspath(os.path.dirname(__file__))
import sys
if sys.version_info < (3,):
    from future import standard_library
    standard_library.install_aliases()
    import tkFileDialog
    import tkMessageBox
else:
    import tkinter.filedialog as tkFileDialog
    import tkinter.messagebox as tkMessageBox

#  Need to redefine object here
# pylint: disable=W0622, W0703, W0612, W0403, C0330
from builtins import object

import tkinter.font
#from tkinter import *
from tkinter import Menu, StringVar, Label, SUNKEN, SW, X, BOTTOM, Frame, NE, NW,\
    BOTH, TOP, Button, LEFT, SE, Scrollbar, VERTICAL, Text, RIGHT, Y, END, Tk,\
    Canvas, Listbox, Entry, N, S, E, W, YES, Grid, NSEW

from PIL import Image, ImageTk

# for multi-file projects see LICENSE file for authorship info
# for single file projects, insert following information
__author__ = 'Charlie Taylor'
__copyright__ = 'Copyright (c) 2016 Charlie Taylor'
__license__ = 'GPL-3'
exec( open(os.path.join( here,'_version.py' )).read() )  # creates local __version__ variable
__email__ = "cet@appliedpython.com"
__status__ = "3 - Alpha" # "3 - Alpha", "4 - Beta", "5 - Production/Stable"

from plot_area import PlotArea        

class Point( object ):
    def __init__(self, x, y):
        
        self.x = x
        self.y = y
        
    def get_str(self):
        return '%g, %g'%(self.x, self.y)
    
    def set_xy(self, x, y):
        self.x = x
        self.y = y
    
    def get_xy(self):
        return self.x, self.y

class DigiPlot(object):
    """A tkinter code that helps users digitize curves from plot images."""

    def __init__(self, master):
        
        self.initComplete = 0
        
        self.frame = Frame(master, width=555, height=546)
        self.frame.pack(fill=BOTH, expand=YES)
        self.master = master
        self.x, self.y, self.w, self.h = -1,-1,-1,-1

        # bind master to <Configure> in order to handle any resizing, etc.
        # postpone self.master.bind("<Configure>", self.Master_Configure)
        self.master.bind('<Enter>', self.bindConfigure)
        #self.master.bind('<Button-1>', self.bindConfigure)
        
        
        self.master.title("DigiPlot")
        
        # ======================  Make a Grid-Oriented Frame =============
        Grid.rowconfigure(master, 1, weight=1)
        Grid.columnconfigure(master, 1, weight=1)


        self.Defined_Points_Label = Label(self.frame,text="Defined Points", width="15")
        self.Defined_Points_Label.grid(row=0, column=0, in_=self.frame)

        # Listbox for points
        lbframe = Frame( self.frame )
        self.Defined_Points_Listbox_frame = lbframe
        scrollbar = Scrollbar(lbframe, orient=VERTICAL)
        self.Defined_Points_Listbox = Listbox(lbframe, width="35", selectmode="extended", 
                                              yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.Defined_Points_Listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.Defined_Points_Listbox.pack(side=LEFT, fill=BOTH)#, expand=YES)
        self.Defined_Points_Listbox_frame.grid(row=1, column=0, sticky="ns", in_=self.frame)
        self.Defined_Points_Listbox.bind("<ButtonRelease-1>", self.Defined_Points_Listbox_Click)

        # Canvas for plot
        self.Plot_Canvas = Canvas(self.frame,width="400", height="400")
        self.Plot_Canvas.grid(row=1, column=1, sticky=NSEW, in_=self.frame)
        self.Plot_Canvas.bind("<ButtonRelease-1>", self.Plot_Canvas_Click)
        self.Plot_Canvas.bind("<Configure>", self.Plot_Canvas_Resize)



        # ======================  End of Grid-Oriented Frame =============
        # make a Status Bar
        self.statusMessage = StringVar()
        self.statusMessage.set("")
        self.statusbar = Label(self.master, textvariable=self.statusMessage, bd=1, relief=SUNKEN)
        self.statusbar.pack(anchor=SW, fill=X, side=BOTTOM)
        
        self.statusMessage.set("Welcome to temp")
        # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "menuStructure"
        self.menuBar = Menu(self.master, relief = "raised", bd=2)

        top_File = Menu(self.menuBar, tearoff=0)

        top_File.add("command", label = "Import Image", command = self.menu_File_Import_Image)
        top_File.add("command", label = "Save CSV", command = self.menu_File_Save_CSV)
        self.menuBar.add("cascade", label="File", menu=top_File)

        top_Anchor_Plot = Menu(self.menuBar, tearoff=0)

        top_Anchor_Plot.add("command", label = "Set Xmin", command = self.menu_Anchor_Plot_Set_Xmin)
        top_Anchor_Plot.add("command", label = "Set Xmax", command = self.menu_Anchor_Plot_Set_Xmax)
        top_Anchor_Plot.add("command", label = "Set Ymin", command = self.menu_Anchor_Plot_Set_Ymin)
        top_Anchor_Plot.add("command", label = "Set Ymax", command = self.menu_Anchor_Plot_Set_Ymax)
        self.menuBar.add("cascade", label="Anchor Plot", menu=top_Anchor_Plot)
        self.menuBar.add("command", label = "Help", command = self.menu_Help)

        top_Exit = Menu(self.menuBar, tearoff=0)

        top_Exit.add("command", label = "Quit", command = self.menu_Exit_Quit)
        self.menuBar.add("cascade", label="Exit", menu=top_Exit)

        self.master.config(menu=self.menuBar)
        
        self.master.sizefrom(who='program')
        self.master.resizable(True, True) # Linux may not respect this

        self.Plot_Canvas.focus_set()
            
        self.PA = PlotArea(w_canv=400, h_canv=400) # will hold PlotArea() when it is opened
        self.pointL = []
            
        
        # give a few milliseconds before calling bindConfigure
        self.master.after(100, lambda: self.bindConfigure(None))

    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "Master_Configure"
    def bindConfigure(self, event):
        if not self.initComplete:
            self.initComplete = 1
            #self.Plot_Canvas.config(width=600, height=500)
            self.master.bind("<Configure>", self.Master_Configure)
            self.plot_points()


    def Master_Configure(self, event):
        
        if event.widget != self.master:
            if self.w > -1:
                return
        self.master.unbind('<Enter>')
            
        x = int(self.master.winfo_x())
        y = int(self.master.winfo_y())
        w = int(self.master.winfo_width())
        h = int(self.master.winfo_height())
        
        if (self.x, self.y, self.w, self.h) == (-1,-1,-1,-1):
            self.x, self.y, self.w, self.h = x,y,w,h
            self.lb_init_width  = int(self.Defined_Points_Listbox_frame.winfo_width() )
            self.lb_init_height = int(self.Defined_Points_Listbox_frame.winfo_height())
            self.w_init = w
            self.h_init = h
            self.w_canv_init = int( self.Plot_Canvas.winfo_width() )

        if self.w!=w or self.h!=h:
            print( "Master reconfigured... make resize adjustments")
            self.w=w
            self.h=h
        
        print('self.frame.w =', self.frame.winfo_width())
        self.frame.update()
        self.frame.update_idletasks()
        
        #dw = max(100, self.w - self.w_init + self.w_canv_init - 1)
        #dh = max(100, self.h - self.h_init + self.lb_init_height)
        
        #self.Plot_Canvas.config(width=dw, height=dh)
        
        #self.PA.set_canvas_wh(dw, dh)
        #self.plot_points()

    def Plot_Canvas_Resize(self, event):
        self.PA.set_canvas_wh(event.width, event.height)
        self.plot_points()
        

    def plot_points(self):
        s = 3
        s2 = s+3
        s3 = s+5
        
        # make coordinate axes
        self.Plot_Canvas.delete("all")
        
        self.photo_image = self.PA.get_tk_photoimage(greyscale=False)
        self.Plot_Canvas.create_image(0,0, anchor=NW, image=self.photo_image )
                                       
        img_slice_resized = self.PA.get_zoomed_offset_img(greyscale=True)
        #print('img_slice_resized.size=',img_slice_resized.size)
                    
        iL = [i for i in self.Defined_Points_Listbox.curselection()]
        if (len(iL)>0):
            isel = iL[0]
        else:
            isel = -1

        # Show points
        for ip,P in enumerate(self.pointL):
            x,y = P.get_xy()
            i,j = self.PA.get_ij_at_xy( x,y )
            
            if min(i,j)>=0:
                if (isel>=0) and (ip==isel):
                    self.Plot_Canvas.create_rectangle((i-s2, j-s2, i+s2, j+s2), outline="black", fill="orange")
                else:
                    self.Plot_Canvas.create_rectangle((i-s2, j-s2, i+s2, j+s2), outline="blue", fill="cyan")
                
    
    def add_point(self, x_float, y_float):
        
        itemL = list(self.Defined_Points_Listbox.get(0, END))
        iL = [i for i in self.Defined_Points_Listbox.curselection()]
        
        if len(itemL)==0:
            self.pointL.append( Point(x_float, y_float) )
            self.Defined_Points_Listbox.insert(END, self.pointL[-1].get_str() )
            self.select_pointL(0)
        else:
            
            if len(iL)==0:
                self.pointL.append( Point(x_float, y_float) )
                self.Defined_Points_Listbox.insert(END, self.pointL[-1].get_str() )
                self.select_pointL(END)
            else:
                self.pointL.insert(iL[0]+1, Point(x_float, y_float) )
                self.Defined_Points_Listbox.insert(iL[0]+1, self.pointL[iL[0]+1].get_str() )
                self.select_pointL(iL[0]+1)
                
                #print( 'self.pointL =',self.pointL)
                
        self.statusMessage.set("added point x,y=%g, %g"%(x_float, y_float))
                
    def select_pointL(self, i ):
        
        self.Defined_Points_Listbox.selection_clear(0, END)
        if i==END:
            self.Defined_Points_Listbox.select_set( END )
            i = len(self.pointL)-1
        else:
            self.Defined_Points_Listbox.select_set( i )
            
        self.plot_points()

    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "menu_File_Import_Image"
    def menu_File_Import_Image(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_File_Import_Image"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_File_Import_Image")
        print( "called menu_File_Import_Image")


    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "menu_File_Save_CSV"
    def menu_File_Save_CSV(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_File_Save_CSV"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_File_Save_CSV")
        print( "called menu_File_Save_CSV")


    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "menu_Anchor_Plot_Set_Xmin"
    def menu_Anchor_Plot_Set_Xmin(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_Anchor_Plot_Set_Xmin"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_Anchor_Plot_Set_Xmin")
        print( "called menu_Anchor_Plot_Set_Xmin")


    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "menu_Anchor_Plot_Set_Xmax"
    def menu_Anchor_Plot_Set_Xmax(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_Anchor_Plot_Set_Xmax"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_Anchor_Plot_Set_Xmax")
        print( "called menu_Anchor_Plot_Set_Xmax")


    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "menu_Anchor_Plot_Set_Ymin"
    def menu_Anchor_Plot_Set_Ymin(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_Anchor_Plot_Set_Ymin"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_Anchor_Plot_Set_Ymin")
        print( "called menu_Anchor_Plot_Set_Ymin")


    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "menu_Anchor_Plot_Set_Ymax"
    def menu_Anchor_Plot_Set_Ymax(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_Anchor_Plot_Set_Ymax"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_Anchor_Plot_Set_Ymax")
        print( "called menu_Anchor_Plot_Set_Ymax")


    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "menu_Help"
    def menu_Help(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_Help"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_Help")
        print( "called menu_Help")


    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "menu_Exit_Quit"
    def menu_Exit_Quit(self):
        pass
        # >>>>>>insert any user code below this comment for section "menu_Exit_Quit"
        # replace, delete, or comment-out the following
        self.statusMessage.set("called menu_Exit_Quit")
        print( "called menu_Exit_Quit")
        self.quit()

    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "compID=1"
    def Plot_Canvas_Click(self, event): #click method for component ID=1
        pass
        # >>>>>>insert any user code below this comment for section "compID=1"
        # replace, delete, or comment-out the following
        
        self.plot_points()
        
        #print( "executed method Plot_Canvas_Click")
        #self.statusMessage.set("executed method Plot_Canvas_Click")
        #print( "clicked in canvas at i,j =",event.x,event.y)
        
        x,y = self.PA.get_xy_at_ij(event.x, event.y)
        #print('x=%g, y=%g'%(x,y))
        self.add_point(x,y)

    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "compID=2"
    def Defined_Points_Listbox_Click(self, event): #click method for component ID=2
        pass
        # >>>>>>insert any user code below this comment for section "compID=2"
        # replace, delete, or comment-out the following
        print( "executed method Defined_Points_Listbox_Click")
        self.statusMessage.set("executed method Defined_Points_Listbox_Click")
        print( "current selection(s) =",self.Defined_Points_Listbox.curselection())
        labelL = []
        for i in self.Defined_Points_Listbox.curselection():
            labelL.append( self.Defined_Points_Listbox.get(i))
        print( "current label(s) =",labelL)
        # use self.Defined_Points_Listbox.insert(0, "item zero")
        #     self.Defined_Points_Listbox.insert(index, "item i")
        #            OR
        #     self.Defined_Points_Listbox.insert(END, "item end")
        #   to insert items into the list box

    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "standard_message_dialogs"

    # standard message dialogs... showinfo, showwarning, showerror
    def ShowInfo(self, title='Title', message='your message here.'):
        tkMessageBox.showinfo( title, message )
        return
    def ShowWarning(self, title='Title', message='your message here.'):
        tkMessageBox.showwarning( title, message )
        return
    def ShowError(self, title='Title', message='your message here.'):
        tkMessageBox.showerror( title, message )
        return
        
    # standard question dialogs... askquestion, askokcancel, askyesno, or askretrycancel
    # return True for OK, Yes, Retry, False for Cancel or No
    def AskYesNo(self, title='Title', message='your question here.'):
        return tkMessageBox.askyesno( title, message )
    def AskOK_Cancel(self, title='Title', message='your question here.'):
        return tkMessageBox.askokcancel( title, message )
    def AskRetryCancel(self, title='Title', message='your question here.'):
        return tkMessageBox.askretrycancel( title, message )
        
    # return "yes" for Yes, "no" for No
    def AskQuestion(self, title='Title', message='your question here.'):
        return tkMessageBox.askquestion( title, message )
    # END of standard message dialogs

    # >>>>>>insert any user code below this comment for section "standard_message_dialogs"


    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "standard_file_dialogs"
    # standard file dialogs... askdirectory, askopenfile, asksaveasfilename

    # return a string containing directory name
    def AskDirectory(self, title='Choose Directory', initialdir="."):
        dirname = tkFileDialog.askdirectory(parent=self.master,initialdir=initialdir,title=title)
        return dirname # <-- string
        
    # return an OPEN file type object OR None (opened using mode, 'r','rb','w','wb')
    # WARNING... opening file with mode 'w' or 'wb' will erase contents
    def AskOpenFile(self, title='Choose File', mode='rb', initialdir='.', filetypes=None):
        if filetypes==None:
            filetypes = [
                ('Text File','*.txt'),
                ('Data File','*.dat'),
                ('Output File','*.out'),
                ('Any File','*.*')]
        fileobj = tkFileDialog.askopenfile(parent=self.master,mode=mode,title=title,
            initialdir=initialdir, filetypes=filetypes)
        
        # if opened, then fileobj.name contains the name string
        return fileobj # <-- an opened file, or the value None
        
    # return a string containing file name (the calling routine will need to open the file)
    def AskSaveasFilename(self, title='Save File', filetypes=None, initialfile=''):
        if filetypes==None:
            filetypes = [
                ('Text File','*.txt'),
                ('Data File','*.dat'),
                ('Output File','*.out'),
                ('Any File','*.*')]

        fileName = tkFileDialog.asksaveasfilename(parent=self.master,filetypes=filetypes, initialfile=initialfile ,title=title)
        return fileName # <-- string
        
    # END of standard file dialogs

    # >>>>>>insert any user code below this comment for section "standard_file_dialogs"


# tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "end"

def main():
    root = Tk()
    app = DigiPlot(root)
    root.mainloop()

if __name__ == '__main__':
    main()
