
import os, sys
import base64
import fnmatch
import mimetypes

def build_py_resource( source_dir, py_out_prefix='myqt', glob_desc='*' ):
    
    parent_dir, res_dir = os.path.split( source_dir )
    print 'parent_dir =',parent_dir
    print '  res_dir  =',res_dir

    py_out_files = '%s_%s_resource_files.py'%(py_out_prefix, res_dir)
    pyOut_files = open(py_out_files,'w')
    pyOut_files.write('''

# parent_dir = %s
target_dir = r"%s"

file_typeD = {} # file type description. index=resource path, value=mime type
'''%(parent_dir, res_dir))
    
    py_out_file_data = '%s_%s_resources.py'%(py_out_prefix, res_dir)
    pyOut_file_data = open(py_out_file_data,'w')

    pyOut_file_data.write('''

import base64

# parent_dir = %s
target_dir = r"%s"

file_dataD = {} # file data dict. index=resource path, value=file contents

'''%(parent_dir, res_dir))
    
    fileL = rec_glob(source_dir, glob_desc)
    for fname in fileL:
        mime = mimetypes.guess_type(fname)
        rel_path = os.path.relpath( fname, source_dir )
        resrc_path = rel_path # os.path.join( res_dir, rel_path )
        print mime, resrc_path
        
        image_file = open(fname, 'rb')
        encoded_string = base64.b64encode(image_file.read())
        image_file.close()

        pyOut_files.write( 'file_typeD[r"%s"]="%s"\n'%(resrc_path,mime))
        pyOut_file_data.write( '\n\nfile_dataD[r"%s"]="""\n'%resrc_path)
        i = 0
        while i < len(encoded_string):
            pyOut_file_data.write( encoded_string[i:i+76] + '\n' )
            i += 76
        pyOut_file_data.write( '"""\n\n' )
        
        
    pyOut_file_data.close()
    pyOut_files.close()
        


def rec_glob_get_dirs(path):
    d=[]
    try:
        for i in os.listdir(path):
            if os.path.isdir(path+i):
                d.append(os.path.basename(i))
    except:pass
    return d

def rec_glob(path,mask):
    l=[]
    if path[-1]!='\\':
        path=path+'\\'
    for i in rec_glob_get_dirs(path):
        l=l+rec_glob(path+i,mask)
    try:
        for i in os.listdir(path):
            ii=i
            i=path+i
            if os.path.isfile(i):
                if fnmatch.fnmatch(ii,mask):
                    l.append(i)
    except:pass
    return l


if __name__ == '__main__':
    
    source_dir = r'D:\py_proj_2017\DigiPlot\digiplot\backup'
    build_py_resource( source_dir, py_out_prefix='digiplot', glob_desc='samp*.png' )
    
    
    