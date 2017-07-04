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
    BOTH, TOP, Button, W, LEFT, SE, Scrollbar, VERTICAL, Text, RIGHT, Y, END, Tk,\
    Canvas, Listbox, Entry

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

class DigiPlot(object):
    """A tkinter code that helps users digitize curves from plot images."""

    def __init__(self, master):
        self.initComplete = 0
        frame = Frame(master, width=1020, height=760)
        self.frame = frame
        frame.pack()
        self.master = master
        self.x, self.y, self.w, self.h = -1,-1,-1,-1
        
        # bind master to <Configure> in order to handle any resizing, etc.
        # postpone self.master.bind("<Configure>", self.Master_Configure)
        self.master.bind('<Enter>', self.bindConfigure)
        

        self.master.title("DigiPlot")


        self.Xmax_Entry = Entry(self.master,width="15")
        self.Xmax_Entry.place(x=64, y=52, width=96, height=21)
        self.Xmax_Entry_StringVar = StringVar()
        self.Xmax_Entry.configure(textvariable=self.Xmax_Entry_StringVar)
        self.Xmax_Entry_StringVar.set("10")
        self.Xmax_Entry_StringVar_traceName = self.Xmax_Entry_StringVar.trace_variable("w", self.Xmax_Entry_StringVar_Callback)

        self.Xmin_Entry = Entry(self.master,width="15")
        self.Xmin_Entry.place(x=64, y=12, width=96, height=21)
        self.Xmin_Entry_StringVar = StringVar()
        self.Xmin_Entry.configure(textvariable=self.Xmin_Entry_StringVar)
        self.Xmin_Entry_StringVar.set("-10")
        self.Xmin_Entry_StringVar_traceName = self.Xmin_Entry_StringVar.trace_variable("w", self.Xmin_Entry_StringVar_Callback)

        self.Ymax_Entry = Entry(self.master,width="15")
        self.Ymax_Entry.place(x=64, y=132, width=95, height=20)
        self.Ymax_Entry_StringVar = StringVar()
        self.Ymax_Entry.configure(textvariable=self.Ymax_Entry_StringVar)
        self.Ymax_Entry_StringVar.set("10")
        self.Ymax_Entry_StringVar_traceName = self.Ymax_Entry_StringVar.trace_variable("w", self.Ymax_Entry_StringVar_Callback)

        self.Ymin_Entry = Entry(self.master,width="15")
        self.Ymin_Entry.place(x=64, y=92, width=95, height=20)
        self.Ymin_Entry_StringVar = StringVar()
        self.Ymin_Entry.configure(textvariable=self.Ymin_Entry_StringVar)
        self.Ymin_Entry_StringVar.set("-10")
        self.Ymin_Entry_StringVar_traceName = self.Ymin_Entry_StringVar.trace_variable("w", self.Ymin_Entry_StringVar_Callback)

        self.Label_1 = Label(self.master,text="Xmin", width="15")
        self.Label_1.place(x=12, y=12, width=30, height=22)

        self.Label_2 = Label(self.master,text="Xmax", width="15")
        self.Label_2.place(x=12, y=52, width=30, height=22)

        self.Label_3 = Label(self.master,text="Ymin", width="15")
        self.Label_3.place(x=12, y=92, width=30, height=22)

        self.Label_4 = Label(self.master,text="Ymax", image="", width="15")
        self.Label_4.place(x=12, y=132, width=30, height=22)



        self.Canvas_1 = Canvas(self.master, width="764", height="720")
        self.Canvas_1.place(x=240, y=12)
        self.Canvas_1.bind("<Button-1>", self.Canvas_1_Click)
        
        self.Canvas_1.bind("<Motion>", self.Canvas_Hover)
        self.Canvas_1.bind("<Button-3>", self.Canvas_Find_Closest)
        self.Canvas_1.bind("<B3-Motion>", self.Canvas_Drag_Axes)


        lbframe = Frame( self.master )
        self.Listbox_1_frame = lbframe
        scrollbar = Scrollbar(lbframe, orient=VERTICAL)
        self.Listbox_1 = Listbox(lbframe, width="15", selectmode="single", 
                                 yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.Listbox_1.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.Listbox_1.pack(side=LEFT, fill=BOTH, expand=1)

        self.Listbox_1_frame.place(x=12, y=432, width=160, height=250)
        self.Listbox_1.bind("<ButtonRelease-1>", self.Listbox_1_Click)
        self.Listbox_1.bind("<Double-Button-1>", self.Listbox_1_DoubleClick)


        # make a Status Bar
        self.statusMessage = StringVar()
        self.statusMessage.set("")
        self.statusbar = Label(self.master, textvariable=self.statusMessage, bd=1, relief=SUNKEN)
        self.statusbar.pack(anchor=SW, fill=X, side=BOTTOM)
        self.menuBar = Menu(master, relief = "raised", bd=2)

        top_File = Menu(self.menuBar, tearoff=0)

        top_File.add("command", label = "Open", command = self.menu_Img_File_Open)
        top_File.add("command", label = "Save", command = self.menu_File_Save)
        self.menuBar.add("cascade", label="File", menu=top_File)

        self.menuBar.add_command(label='Help', command=self.help_popup)

        master.config(menu=self.menuBar)
        master.bind('<Escape>', self.Clear_Pending_Actions)


        
        self.w_canv = int(self.Canvas_1.cget("width"))
        self.h_canv = int(self.Canvas_1.cget("height"))
        
        self.Canvas_1.config( bg='#ddffff' )
        self.canvas_bg_img = None # Use Background/Import menu
        self.canvas_bg_photo = None # Needed by Canvas object (ImageTk.PhotoImage)
        self.canvas_bg_img_is_greyscale = False
        self.canvas_bg_img_x_offset = 0
        self.canvas_bg_img_y_offset = 0


        # =========================== 
        self.PA = PlotArea(w_canv=self.w_canv, h_canv=self.h_canv) # will hold PlotArea() when it is opened
        self.pointL = []

        
        self.last_right_click_pos = (0,0) # any action calling Canvas_Find_Closest will set
        self.last_right_click_bbox = (self.PA.x_origin, self.PA.xmax, self.PA.y_origin, self.PA.ymax)
        
        self.pathopen = ''
        self.fopen = ''
        self.dirname = ''
        if len( sys.argv ) == 2:
            fName = sys.argv[1]
            if fName.find('.')<0:
                fName += '.png'
            self.pathopen = os.path.abspath(fName)
            if os.path.isfile( self.pathopen ): # if file exists, read it as a definition file
                
                self.canvas_bg_img_is_greyscale = False
                
                self.PA.open_img_file( self.pathopen )
                
                self.canvas_bg_photo = self.PA.get_tk_photoimage(greyscale=self.canvas_bg_img_is_greyscale)
                self.plot_points()
            else:
                MainWin.statusMessage.set('file "%s" does not exist'%fName)
        
        

    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "menu_Img_File_Open"
    def menu_Img_File_Open(self):
        self.statusMessage.set("called menu_Img_File_Open")
        print( "called menu_Img_File_Open")
        
        self.statusMessage.set("called menu_Background_Import_PNG")
        
        filetypes = [
            ('PNG Image','*.png'),
            ('Any File','*.*')]
        img_path = tkFileDialog.askopenfilename(parent=self.master,title='Open Image file', 
            filetypes=filetypes)
            
        if img_path:
            self.canvas_bg_img_is_greyscale = False
            
            self.PA.open_img_file( img_path )
            if self.PA.img is not None:
                self.canvas_bg_photo = self.PA.get_tk_photoimage(greyscale=self.canvas_bg_img_is_greyscale)
            self.plot_points()

    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "menu_File_Save"
    def menu_File_Save(self):
        self.statusMessage.set("called menu_File_Save")
        print( "called menu_File_Save")
        
        if self.pathopen:
            name = self.fopen
        else:
            name = '*.csv'
        self.saveFile(name)
        
    def saveFile(self, fileDesc='*.csv'):
        print( 'Save File')
        fsave = tkFileDialog.asksaveasfilename(parent=self.master, title='Saving Perimeter or Path file', 
            initialfile=fileDesc)
        
        if fsave:
            if fsave.find('.')<0:
                fsave += '.csv'
            
            
            self.pathopen = fsave
            self.set_file_properties()
            print( 'Saving to:',self.fopen)
            
            self.master.title("tk_perimeter: %s"%self.fopen)
            
            fOut = open( self.pathopen, 'w' )
            
            for P in self.pointL:
                fOut.write( '%s\n'%P.get_str() )
                #print 'Saving Line:',P.get_str()
            fOut.close()

        
    
    def get_floats_from_event_xy(self, event):
        if hasattr(self, 'PA'):
            return self.PA.get_xy_at_ij( event.x, event.y )
        else:
            return None, None
        
        
    def get_canvas_ij(self, x_float, y_float):
        return self.PA.get_ij_at_xy( x_float, y_float )

    def Clear_Pending_Actions(self, event):
        self.statusMessage.set("Cleared pending actions.")
        
        self.is_dragging = False
        
        self.is_dragging_all = False
        self.is_dragging_all_start_posx = 0.0
        self.is_dragging_all_start_posy = 0.0
        
        self.Canvas_1.bind("<Button-1>", self.Canvas_1_Click)
    def bindConfigure(self, event):
        if not self.initComplete:
            self.master.bind("<Configure>", self.Master_Configure)
            self.initComplete = 1


    def Master_Configure(self, event):
        if event.widget != self.master:
            if self.w != -1:
                return
        x = int(self.master.winfo_x())
        y = int(self.master.winfo_y())
        w = int(self.master.winfo_width())
        h = int(self.master.winfo_height())
        if (self.x, self.y, self.w, self.h) == (-1,-1,-1,-1):
            self.x, self.y, self.w, self.h = x,y,w,h


        if self.w!=w or self.h!=h:
            print( "Master reconfigured... make resize adjustments")
            self.w=w
            self.h=h
            
            self.Canvas_1.config( width=w-250, height=h-42 )

        self.w_canv = int(self.Canvas_1.cget("width"))
        self.h_canv = int(self.Canvas_1.cget("height"))
        
        if self.PA.img is not None:
            self.PA.reset_canvas_wh(self.w_canv, self.h_canv)
            self.canvas_bg_photo = self.PA.get_tk_photoimage(greyscale=self.canvas_bg_img_is_greyscale)
            self.plot_points()
        

    def Canvas_Find_Closest(self, event): #click method for component ID=1
        ix = int(event.x)
        iy = int(event.y)   #self.h_canv - int(event.y)
        #print "Right Click event ix,iy=",ix,iy
        
        self.last_right_click_pos = (ix, iy)
        self.last_right_click_bbox = (self.PA.x_origin, self.PA.xmax, self.PA.y_origin, self.PA.ymax)
        
        #dx = max(1.0E-6, abs(self.xmax - self.xmin))
        #dy = max(1.0E-6, abs(self.ymax - self.ymin))
        
        # Find the closest point
        ibest = 0
        dbest = 1.0E12
        for i,P in enumerate( self.pointL ):
            x,y = P.get_xy()
            ii,jj = self.get_canvas_ij(x,y)
            d = (ix-ii)**2 + (iy-jj)**2
            if d<dbest:
                ibest = i
                dbest = d
            
                
        self.select_pointL( ibest )
        
        print( 'ibest=%s'%(ibest, ))
        return ibest


    def Canvas_Hover(self, event):
        x = int(event.x)
        y = self.h_canv - int(event.y)
        
        x_move, y_move = self.get_floats_from_event_xy(event)
        
        try:
            x_str = '%g'%x_move
            y_str = '%g'%y_move
        except:
            x_str = '%s'%x_move
            y_str = '%s'%y_move
            
        
        self.statusMessage.set(x_str + ', ' + y_str)

    def Canvas_Drag_Axes(self, event):
        
        di = event.x - self.last_right_click_pos[0]
        dj = event.y - self.last_right_click_pos[1]
        #print 'Right Drag x,y =',event.x, event.y,'   di,dj=',di,dj
        
        xmin, xmax, ymin, ymax = self.last_right_click_bbox


        dx = -(xmax - xmin) * di / float(self.w_canv)
        dy = (ymax - ymin) * dj / float(self.h_canv)

        xlo = self.get_snap_value( xmin + dx )
        xhi = self.get_snap_value( xmax + dx )

        ylo = self.get_snap_value( ymin + dy )
        yhi = self.get_snap_value( ymax + dy )

        self.Xmin_Entry_StringVar.set( '%g'%xlo )
        self.Xmax_Entry_StringVar.set( '%g'%xhi )
        self.Ymin_Entry_StringVar.set( '%g'%ylo )
        self.Ymax_Entry_StringVar.set( '%g'%yhi )
        
        self.plot_points()

    def Listbox_1_DoubleClick(self, event):
        
        self.EditXYR_Button_Click( event )

        
    def Canvas_1_Click(self, event): #click method for component ID=1
        self.statusMessage.set("executed method Canvas_1_Click")
        x = int(event.x)
        y = self.h_canv - int(event.y)
        x_float, y_float = self.get_floats_from_event_xy(event)
        
        if x_float is not None:
            self.add_point( x_float, y_float)
            
            self.plot_points()
                
    def select_pointL(self, i ):
        
        self.Listbox_1.selection_clear(0, END)
        if i==END:
            self.Listbox_1.select_set( END )
            i = len(self.pointL)-1
        else:
            self.Listbox_1.select_set( i )
            
        self.plot_points()

    def plot_points(self):
        
            
        s = 3
        s2 = s+3
        s3 = s+5
        
        # make coordinate axes
        self.Canvas_1.delete("all")
        
        if self.PA.img is not None:
            self.Canvas_1.create_image(self.canvas_bg_img_x_offset, self.canvas_bg_img_y_offset, 
                                       anchor=NW, image=self.canvas_bg_photo)
                                       
                    
        iL = [i for i in self.Listbox_1.curselection()]
        if (len(iL)>0):
            isel = iL[0]
        else:
            isel = -1

        # Show points
        for ip,P in enumerate(self.pointL):
            x,y = P.get_xy()
            i,j = self.get_canvas_ij( x,y )
            
            if min(i,j)>=0:
                if (isel>=0) and (ip==isel):
                    self.Canvas_1.create_rectangle((i-s2, j-s2, i+s2, j+s2), outline="black", fill="orange")
                else:
                    self.Canvas_1.create_rectangle((i-s, j-s, i+s, j+s), outline="blue", fill="blue")
                
        
    
    def add_point(self, x_float, y_float):
        
        itemL = list(self.Listbox_1.get(0, END))
        iL = [i for i in self.Listbox_1.curselection()]
        
        if len(itemL)==0:
            self.pointL.append( Point(x_float, y_float) )
            self.Listbox_1.insert(END, self.pointL[-1].get_str() )
            #self.Listbox_1.select_set(0)
            self.select_pointL(0)
        else:
            
            if len(iL)==0:
                self.pointL.append( Point(x_float, y_float) )
                self.Listbox_1.insert(END, self.pointL[-1].get_str() )
                #self.Listbox_1.select_set(END)
                self.select_pointL(END)
            else:
                self.pointL.insert(iL[0]+1, Point(x_float, y_float) )
                self.Listbox_1.insert(iL[0]+1, self.pointL[iL[0]+1].get_str() )
                #self.Listbox_1.select_set(iL[0]+1)
                self.select_pointL(iL[0]+1)
                
                #print 'self.pointL =',self.pointL
        
        
    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "compID=15"
    def Listbox_1_Click(self, event): #click method for component ID=15
        #print "executed method Listbox_1_Click"
        self.statusMessage.set("executed method Listbox_1_Click")
        
        iL = [i for i in self.Listbox_1.curselection()]
        if (len(iL)>0):
            self.select_pointL(iL[0])

    def RePlot_Button_Click(self, event):
        self.plot_points()
        

    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "compID=16"
    def Del_Button_Click(self, event): #click method for component ID=16
        #print "executed method Del_Button_Click"
        self.statusMessage.set("executed method Del_Button_Click")
        
        iL = [i for i in self.Listbox_1.curselection()]
        if len(iL)>0:
            #print 'Deleting item %i'%iL[0]
            
            self.Listbox_1.delete( iL[0] )
            self.pointL.pop( iL[0] )
            
            isel = iL[0]-1
            if isel < 0:
                isel = 0
            if len(self.pointL)>0:
                self.select_pointL(isel)
            

        self.plot_points()

    def MouseWheelHandler(self, event):

        if event.num == 5 or event.delta < 0:
            result = -1 
            self.MakeBigger_Button_Click(event)
        else:
            result = 1 
            self.MakeSmaller_Button_Click(event)

        #print 'MouseWheelHandler result =',result

    def MakeBigger_Button_Click(self, event):
        dx = (self.xmax - self.xmin) * 0.1/ 0.8
        xlo = self.xmin - dx
        xhi = self.xmax + dx

        dy = (self.ymax - self.ymin) * 0.1/ 0.8
        ylo = self.ymin - dy
        yhi = self.ymax + dy

        self.Xmin_Entry_StringVar.set( '%g'%xlo )
        self.Xmax_Entry_StringVar.set( '%g'%xhi )

        self.Ymin_Entry_StringVar.set( '%g'%ylo )
        self.Ymax_Entry_StringVar.set( '%g'%yhi )
        
        self.plot_points()
        
    def MakeSmaller_Button_Click(self, event):
        dx = (self.xmax - self.xmin) * 0.1
        xlo = self.xmin + dx
        xhi = self.xmax - dx

        dy = (self.ymax - self.ymin) * 0.1
        ylo = self.ymin + dy
        yhi = self.ymax - dy

        self.Xmin_Entry_StringVar.set( '%g'%xlo )
        self.Xmax_Entry_StringVar.set( '%g'%xhi )
        self.Ymin_Entry_StringVar.set( '%g'%ylo )
        self.Ymax_Entry_StringVar.set( '%g'%yhi )
        
        self.plot_points()
        
    def MakeFit_Button_Click(self, event):
        if len(self.pointL)>0:
            ptL = [pt.get_xy() for pt in self.pointL]
            
            xL = [p[0] for p in ptL]
            yL = [p[1] for p in ptL]
            
            xmin = min(xL)
            xmax = max(xL)
            ymin = min(yL)
            ymax = max(yL)
            
            dx = xmax - xmin
            dy = ymax - ymin
            
            xlo = xmin - dx/10.0
            xhi = xmax + dx/10.0

            ylo = ymin - dy/10.0
            yhi = ymax + dy/10.0
        
            self.Xmin_Entry_StringVar.set( '%g'%xlo )
            self.Xmax_Entry_StringVar.set( '%g'%xhi )
            self.Ymin_Entry_StringVar.set( '%g'%ylo )
            self.Ymax_Entry_StringVar.set( '%g'%yhi )
            
            self.plot_points()

    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "Xmax_Entry_StringVar_Callback"
    def Xmax_Entry_StringVar_Callback(self, varName, index, mode):
        #print "Xmax_Entry_StringVar_Callback varName, index, mode",varName, index, mode
        self.statusMessage.set("    Xmax_Entry_StringVar = "+self.Xmax_Entry_StringVar.get())
        #print "    new StringVar value =",self.Xmax_Entry_StringVar.get()
        
        try:
            self.xmax = float( self.Xmax_Entry_StringVar.get() )
        except:
            pass
            
        self.PA.set_x_max( self.xmax )
        self.plot_points()


    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "Xmin_Entry_StringVar_Callback"
    def Xmin_Entry_StringVar_Callback(self, varName, index, mode):
        #print "Xmin_Entry_StringVar_Callback varName, index, mode",varName, index, mode
        self.statusMessage.set("    Xmin_Entry_StringVar = "+self.Xmin_Entry_StringVar.get())
        #print "    new StringVar value =",self.Xmin_Entry_StringVar.get()
        
        try:
            self.xmin = float( self.Xmin_Entry_StringVar.get() )
        except:
            pass
        self.PA.set_x_origin( self.xmin )
        self.plot_points()


    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "Ymax_Entry_StringVar_Callback"
    def Ymax_Entry_StringVar_Callback(self, varName, index, mode):
        #print "Ymax_Entry_StringVar_Callback varName, index, mode",varName, index, mode
        self.statusMessage.set("    Ymax_Entry_StringVar = "+self.Ymax_Entry_StringVar.get())
        #print "    new StringVar value =",self.Ymax_Entry_StringVar.get()
        
        try:
            self.ymax = float( self.Ymax_Entry_StringVar.get() )
        except:
            pass
        self.PA.set_y_max( self.ymax )
        self.plot_points()


    # tk_happy generated code. DO NOT EDIT THE FOLLOWING. section "Ymin_Entry_StringVar_Callback"
    def Ymin_Entry_StringVar_Callback(self, varName, index, mode):
        #print "Ymin_Entry_StringVar_Callback varName, index, mode",varName, index, mode
        self.statusMessage.set("    Ymin_Entry_StringVar = "+self.Ymin_Entry_StringVar.get())
        #print "    new StringVar value =",self.Ymin_Entry_StringVar.get()
        try:
            self.ymin = float( self.Ymin_Entry_StringVar.get() )
        except:
            pass
        self.PA.set_y_origin( self.ymin )
        self.plot_points()



    def help_popup(self):
        help_msg = """
        
Left Click = Add Point 
Right Click = Select Nearest Point 
Left Double Click List = Edit Point.
Mouse Wheel = Zoom

Esc Key = Clear Pending Actions
"""
        self.ShowInfo( title='Help', message='Mouse/Keyboard Options\r' + help_msg)

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
        

def main():
    """Run Main Window"""
    root = Tk()
    DigiPlot(root)
    root.mainloop()


if __name__ == '__main__':
    main()
