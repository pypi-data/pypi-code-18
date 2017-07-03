#import base64
from Tkinter import *
from digiplot_backup_resources import file_dataD


#base64_str = file_dataD["document.thmb40.png"]
#decoded_str = base64.b64decode( base64_str.replace('\\n','') )

IMAGE_DATA = file_dataD["Cu_cte.gif"]

imgL = []

root = Tk()
for name, img64 in file_dataD.items():
    print name
    image = PhotoImage(data=img64) # ONLY works with gif and PGM/PPM images
    imgL.append( image ) # don't lose reference to image
    label = Label(root, image=image, padx=20, pady=20)
    label.pack(side=LEFT)
    
root.mainloop()


