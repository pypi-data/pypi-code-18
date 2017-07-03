from mzStudio import *

if __name__ == '__main__':
    app = wx.App(False)
    
    import platform
    if 'Windows' in platform.platform():
        import multiplierz.mzAPI.management as api_management
        guids_that_work = api_management.testInterfaces()
        if not all(guids_that_work):
            print "NOTE- One or more vendor file interfaces are not currently installed."
            print "Access to some files may fail."
            print "To fix, run multiplierz.mzAPI.management.registerInterfaces()"
        elif not any(guids_that_work):
            ask_about_mzAPI = """
The multiplierz mzAPI vendor file interface modules
have not been enabled on this machine; these are required
in order to access .RAW, .WIFF and .D files.  Enable now?
(This requires administrator priviledges.)
            """
        
            askdialog = wx.MessageDialog(None, ask_about_mzAPI, 'mzAPI Setup', wx.YES_NO | wx.ICON_QUESTION)
            if askdialog.ShowModal() == wx.ID_YES:
                api_management.registerInterfaces()
                print "Press enter to continue."
                raw_input()    
    
    frame = TopLevelFrame(None)        
    frame.Show()
    
    app.MainLoop()