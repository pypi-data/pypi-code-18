#tkinter-extensions for user interaction.

import sys
if sys.version[0] == '2':
    import Tkinter as tk
    import tkFileDialog as tf
else:
    from functools import reduce
    import tkinter as tk
    import tkinter.filedialog as tf

class WindowOptions(tk.Frame):
    """ This class accepts a list of (sting) choices,
        creates a (tkinter) window with option buttons for each choice,
        waits for the user to select one and press the 'Continue' button
        - or Cancel
    
    Args:
       choicelist:  a list or tuple containing string descriptions of the
                   different choices.
       
    Kwargs:
       master= (tk.Frame instance): parent window frame, if any. Default is
                to create a new independent top-level window
       title= (string): Window title. Default is 'Choose'
       preset= (integer): index integer to pre-select one of the options in
                choicelist. Default is 0

    Returns: 
       <class instance>.get() returns an integer value:
           integer in range(len(choicelist)) # that is 0 ... len(choicelist)-1
               or
           -1    for Cancel or zero-length of choicelist
    Note:
        Calling the .get() function closes and destroys the class WindowOptions
    
    Raises:
       Don't know what surprises are there!

    Sample call:
            inst = WindowCoice(['option 1','text 2], title='Select one', preset=0)
            inst.mainloop()
            index = inst.get()
        Note: calling methode get() closes WindowOptions
    """
    def __init__(self, choicelist, master=None, title='Choose', preset=0):
        if len(choicelist) == 0:
            self.cancel = True
            row = -1
        else:
            self.cancel = False
        tk.Frame.__init__(self, master)
        self.grid()
        self.master.title(title)
        self.choiceVar = tk.IntVar()
        self.choiceVar.set(preset)
        for row,choice in enumerate(choicelist):
            cmd = 'self.Choice{0:02d} = '.format(row)\
                  +'tk.Radiobutton(self, variable=self.choiceVar,'\
                  +"text='" + choice + "', value={0:d})".format(row)
            exec(cmd)
            cmd = 'self.Choice{0:02d}.grid(row={0:d}, column=0, sticky=tk.W)'.format(row)
            exec(cmd)
        row += 1
        self.ButtonQuit = tk.Button(self, text='Cancel',fg='white', bg='black',
                                         command=self.ButtonQuit)
        self.ButtonQuit.grid(row=row, column=0)
        self.ButtonSave = tk.Button(self, text="Continue",
                                         command=self.ButtonStart)
        self.ButtonSave.grid(row=row, column=1)

    def ButtonQuit(self):
        self.cancel = True
        self.quit()

    def ButtonStart(self):
        self.quit()

    def get(self):
        if self.cancel:
            self.master.destroy()
            return -1
        else:
            retn = self.choiceVar.get()
            self.master.destroy()
            return retn                   

class WindowButtons(tk.Frame):
    """ This class accepts a list of (sting) choices,
        creates a (tkinter) window with one button for each choice,
        waits for the user to select one - or Cancel.
        There is no 'Accept' button; clicking on one of the choices is enough.
    
    Args:
       choicelist:  a list or tuple containing string descriptions of the
                   different choices.
       
    Kwargs:
       master= (tk.Frame instance): parent window frame, if any. Default is
                to create a new independent top-level window
       title= (string): Window title. Default is 'Choose'

    Returns: 
       <class instance>.get() returns an integer value:
           integer in range(len(choicelist)) # that is 0 ... len(choicelist)-1
               or
           -1    for Cancel or zero-length of choicelist
    Note:
        Calling the .get() function closes and destroys the class WindowButtons
    
    Raises:
       Don't know what surprises are there!

    Sample call:
            inst = WindowButtons(['option 1','text 2], title='Select one')
            inst.mainloop()
            index = inst.get()
        Note: calling methode get() closes WindowButtons
    """
    def __init__(self, choicelist, master=None, title='Choose'):
        if len(choicelist) == 0:
            self.cancel = True
            row = -1
        else:
            self.cancel = False
        tk.Frame.__init__(self, master)
        self.grid()
        self.master.title(title)
        self.choiceVar = tk.IntVar()
        self.choiceVar.set(0)
        maxwidth = reduce(lambda x,y: max(x, len(y)), choicelist, 0)
        for row,choice in enumerate(choicelist):
            def handler(event, self=self, row=row):
                return self.ButtonHandler(event, row)
            elem = tk.Button(self, text=choice, command=handler, width=maxwidth)
            elem.bind('<Button-1>', handler)
            elem.grid(row=row, column=0)
        row += 1
        self.ButtonQuit = tk.Button(self, text='Cancel',bg='black', fg='white',
                                         command=self.ButtonQuit)
        self.ButtonQuit.grid(row=row, column=0)

    def ButtonHandler(self, event, row):
        self.choiceVar.set(row)
        self.quit()
        
    def ButtonQuit(self):
        self.cancel = True
        self.quit()

    def get(self):
        if self.cancel:
            self.master.destroy()
            return -1
        else:
            retn = self.choiceVar.get()
            self.master.destroy()
            return retn                   

class WindowEntries(tk.Frame):
    """ This class accepts a list of tuples describing each (text) entry.
        Each tuple must contain 4 fields:
           1. a string containing the prompt text (i.e. what is expected)
           2. an integer defining the maximum number of characters allowed
           3. a string containing a pre-set text, if any.
           4. a string containing a comment or unit descriptor, if any
        The class creates a (tkinter) window with one line for each descriptor
        tuple, consisting of the prompt column, entry field column
        and comment/unit descriptor column.
        It waits for the user to fill out all entry columns and press the 'Ok'
        button - or Cancel button.
    
    Args:
       choicelist:  a list or tuple containing descriptor tuples of entries
                    expected. See example below.
       
    Kwargs:
       master= (tk.Frame instance): parent window frame, if any. Default is
                to create a new independent top-level window
       title= (string): Window title. Default is 'Please enter'

    Special: if Comment/Unit text contains 'askdirectory', then
            it will be replaced by a button calling tkFileDialog.askdirectory()
            if Comment/Unit text contains 'asksaveasfilename', then
            it will be replaced by a button calling tkFileDialog.asksaveasfilename()
            
    Returns: 
       <class instance>.get() returns a list of text entries
               or
       [None, .., None]    for Cancel or zero-length of choicelist

    Note:
        Calling the .get() function closes and destroys the class WindowEntries
    
    Raises:
       Don't know what surprises are there!

    Sample call:
            specs = (('Picture Base Directory',75, '/home/franz/',None),
                     ('Subdirectory',24, 'python','askdirectory'),
                     ('Supplier code',4,None,'Empty=all'))
            inst = WindowEntries(specs, title='Enter parameters')
            inst.mainloop()
            index = inst.get()
        Note: calling methode get() closes WindowEntries
    """
    def __init__(self, qlist, master=None, title='Please enter'):
        if len(qlist) == 0:
            qlist = []
            self.cancel = True
            row = -1
        else:
            self.cancel = False
        tk.Frame.__init__(self, master)
        self.grid()
        self.master.title(title)
        self.cancel = False
        self.Vars = []
        for row,entry in enumerate(qlist):
            text, width, preset, tail = entry
            lbl = tk.Label(self, text=text)
            lbl.grid(row=row, column=0, sticky=tk.E)
            var = tk.StringVar()
            if preset is not None and len(preset) > 0:
                var.set(preset)
            self.Vars.append(var)
            entry = tk.Entry(self, width=width, textvariable=var)
            entry.grid(row=row, column=1, sticky=tk.W)
            if tail is not None and len(tail) > 0:
                if tail.find('askdirectory') >= 0:
                    def handler(event, self=self, row=row):
                        return self.ButtonAskDir(event, row)
                    elem = tk.Button(self, text='Find', command=handler)
                    elem.bind('<Button-1>', handler)
                elif tail.find('asksaveasfilename') >= 0:
                    def handler(event, self=self, row=row):
                        return self.ButtonFilename(event, row)
                    elem = tk.Button(self, text='Find', command=handler)
                    elem.bind('<Button-1>', handler)
                else:
                    elem = tk.Label(self, text=tail)
                elem.grid(row=row, column=2, sticky=tk.W)
        row += 1
        self.ButtonQuit = tk.Button(self, text='Cancel', command=self.ButtonQuit,
                                    fg='white', bg='black')
        self.ButtonQuit.grid(row=row, column=0)
        self.ButtonSave = tk.Button(self, text="Ok", command=self.ButtonStart)
        self.ButtonSave.grid(row=row, column=2)

    def ButtonAskDir(self, event, row):
        sdir = tf.askdirectory()
        self.Vars[row].set(sdir)

    def ButtonFilename(self, event, row):
        sdir = tf.asksaveasfilename()
        self.Vars[row].set(sdir)

    def ButtonQuit(self):
        self.cancel = True
        self.quit()

    def ButtonStart(self):
        self.quit()

    def get(self):
        if self.cancel:
            retn = [ None for s in self.Vars ]
        else:
            retn = [ s.get() for s in self.Vars]
        self.master.destroy()
        return retn

if __name__ == '__main__':        # test the stuff
    textlist = ['x line 1','y another one','z and so on']
#    textlist = []
    inst = WindowOptions(textlist, title='Test')
    inst.mainloop()
    print(inst.get())

    textlist = ['x line 1','y another one','z and so on']
#    textlist = []
    inst = WindowButtons(textlist, title='Test')
    inst.mainloop()
    print(inst.get())

    specs = (('Picture Base Directory',75, '/home/franz','askdirectory'),
             ('Subdirectory',24, 'python','asksaveasfilename'),
             ('Supplier code',4,None,'Empty=all'))
#    specs = ()

    inst = WindowEntries(specs, title='Enter')
    inst.mainloop()
    print(inst.get())

