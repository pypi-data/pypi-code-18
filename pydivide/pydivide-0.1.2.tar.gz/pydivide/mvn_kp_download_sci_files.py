###############################################################################
#
#Download Files Section
#
###############################################################################

from . import mvn_kp_download_files_utilities as utils
from .mvn_kp_utilities import orbit_time
from dateutil.parser import parse

def mvn_kp_download_sci_files(filenames=None, 
                              instruments=None,
                              level='l2',
                              list_files=False, 
                              new_files=False, 
                              start_date='2014-01-01', 
                              end_date='2020-01-01', 
                              update_prefs=False,
                              only_update_prefs=False, 
                              exclude_orbit_file=False,
                              local_dir=None,
                              help=False,
                              unittest=False):
    
    import os
    
    #Check for orbit num rather than time string
    if isinstance(start_date, int) and isinstance(end_date, int):
        start_date, end_date = orbit_time(start_date, end_date)
        start_date = parse(start_date)
        end_date = parse(end_date)
        start_date = start_date.replace(hour=0, minute=0, second=0)
        end_date = end_date.replace(day=end_date.day+1, hour=0, minute=0, second=0)
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')  

    if (update_prefs==True or only_update_prefs==True):
        utils.set_root_data_dir()
        if (only_update_prefs==True):
            return
    
    public = utils.get_access()
    if (public==False):
        utils.get_uname_and_password()

    if (filenames != None):
        if (instruments == None):
            print("Must specify an instrument.")
            print("lpw, ngi, euv, sta, swi, swe, mag, iuv, sep")
            return
        if (level == None):
            print("Must specify a data level.")
            print("l1a, l1b, l1c, l2, or l3")
            return
    for instrument in instruments:
        # Build the query to the website
        query_args=[]
        query_args.append("instrument="+instrument)
        query_args.append("level="+str(level))
        if (filenames!=None):
            query_args.append("file="+filenames)
        query_args.append("start_date="+start_date)
        query_args.append("end_date="+end_date)
    
        if local_dir == None:
            mvn_root_data_dir = utils.get_root_data_dir()
        else:
            mvn_root_data_dir = local_dir
        
        data_dir   = os.path.join(mvn_root_data_dir,'maven','data','sci',instrument,level)     
        
        query = '&'.join(query_args)
        
        s = utils.get_filenames(query, public)
        
        if (len(s)==0):
            print("No files found.")
            continue
        
        s = s.split(',')
        
        if (list_files==True):
            for f in s:
                print(f)
            continue
        
        if (new_files==True):
            s = utils.get_new_files(s, data_dir, instrument, level)
            
        if (len(s)==0):
            print("No files found.")
            return
        if not unittest:
            print("Your request will download a total of "+str(len(s))+" files for instrument "+str(instrument))
            print('Would you like to procede with the download: ')
            valid_response=False
            while(valid_response==False):
                response = (input('(y/n) >'))
                if response=='y' or response=='Y':
                    valid_response=True
                    cancel=False
                elif response=='n' or response=='N':
                    print('Cancelled download. Returning...')
                    valid_response=True
                    cancel=True
                else:
                    print('Invalid input.  Please answer with y or n.')
        
        if cancel:
            continue
        
        if exclude_orbit_file == False:
            print("Before downloading data files, checking for updated orbit # file from naif.jpl.nasa.gov")
            print("")
            utils.get_orbit_files()
        
        i=0
        utils.display_progress(i, len(s))
        for f in s:
            i = i+1
            full_path = utils.create_dir_if_needed(f, data_dir, level)
            utils.get_file_from_site(f, public, full_path)
            utils.display_progress(i, len(s))
    
     
    return


    