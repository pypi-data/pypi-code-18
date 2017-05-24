from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

try:
    from packageskel import wingdbstub
except ImportError as e:
    print("Failed to import wingdbstub")
    

from pathlib import Path
import os
import argparse
import sys
import shutil
import os
import logging
import logging.config
import re

from future.utils import PY3


LOGGING_CONFIG = { 
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': { 
        'standard': { 
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': { 
        'default': { 
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': { 
        '': { 
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        'PackageSkel': { 
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
    } 
}
logging.config.dictConfig(LOGGING_CONFIG)


class PackageSkel(object):
    """
    A class that copies the package skeleton to the desired 
    destination path.
    """
    
    def _rename_file(self, filepath):
        pass
    
    def _rename_dir(self, dirpath):
        pass
    
    def process_node(self, path):    
        """
        Iterates over a directory and renames all occourences of the 
        template package skeleton to the new package name
        """
        #is node a file?
        if not isinstance(path, Path):
            path = Path(path)
        #is node a dir?
        if path.is_dir():
            #iterate over the contents of the directory
            for node in path.iterdir():
                self.process_node(node)
            #now rename this directory too if needed. 
            self.logger.debug("Leaving dir: {}".format(path.as_posix()))
        
        subject = path.name   
        result = re.match(r"([\w\d]*)(packageskel)([\w\d\.]*)", subject)

        if result:
            #We always end up with 3 results
            group0 = result.groups()[0]
            group1 = result.groups()[1]
            group2 = result.groups()[2]
            new_path = Path(path.parent, "{}{}{}".format(group0, self.package_name, group2))                
            
            if path.as_posix().endswith(".pyc"):
                #quietly delete any .pyc files.
                os.remove(path.as_posix())
            else:
                print("{} --> {}".format(path, new_path))
                os.rename(path.as_posix(), new_path.as_posix())
                
    def copy_skeleton(self):
        """
        This just copies the whole template directory 
        into the destination directory.
        """    
        
        dirpath = Path(self.destination_path, self.package_name)
        if dirpath.exists():
            self.logger.debug("{} exists. Going to delete it.".format(dirpath))
            shutil.rmtree(dirpath.as_posix())
        
        self.logger.debug("Going to copy skeleton to: {}".format(dirpath))    
        shutil.copytree(self.templates_dir.as_posix(), dirpath.as_posix())
        self.process_node(dirpath)
        
    def _get_default_templates_dir(self):
        file_path = os.path.abspath(__file__)
        file_dir, file_name = os.path.split(file_path)    
        return Path(os.path.join(file_dir,"templates","default"))
    
    
    
    def __init__(self, package_name, destination_path=None):
        """
        Accepts the package_name and an optional destination_path 
        parameter.
        
        :param package_name: Name of the package to create
        :type package_name: string
        :param destination_path: Path where to create the package. This can be relative or absolute posix path.
        :type destination_path: str 
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.package_name = package_name
        
        
        if destination_path is None:
            #We just decide to build the package in the current working dir
            #if the user does not give us a destination_path
            destination_path = os.path.basename(os.getcwd())
            
        
        if not isinstance(destination_path, Path):
            #ensure that paths is of type Path
            destination_path = Path(destination_path)
            
        self.destination_path = destination_path
        
        
        #templates_dir is hardcoded currenlty to default and 
        #need to rename anything that starts with packageskel
        self.templates_dir = self._get_default_templates_dir()
        
    

def make_template():

    try:
        package_name = sys.argv[1]
    except IndexError as e:
        print("Package name is required.")
        sys.exit()

    destination_path = os.getcwd()
    print("Going to create package skeleton in : {}".format(destination_path))

    pskel = PackageSkel(package_name, destination_path)

    pskel.copy_skeleton()
    #print("{} already exists as a directory. Aborting.".format(package_name))


if __name__ == "__main__":



    make_template()
