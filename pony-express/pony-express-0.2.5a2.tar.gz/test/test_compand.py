import unittest 

import os
import shutil
import io

import pony
from test.facilities import ensure_path, touch



class TestStringMethods(unittest.TestCase):

    def setUp(self):
        """Create an input folder structure"""
        print ('setting up')
        ensure_path('test/temp-data/subfolder/subsubfolder')
        touch('test/temp-data/one.txt')
        touch('test/temp-data/two.txt')
        touch('test/temp-data/subfolder/ignore.tx')
        touch('test/temp-data/subfolder/three.txt')
        touch('test/temp-data/subfolder/subsubfolder/four.txt')

    def tearDown(self):
        """Destroy temporary folder structure"""
        shutil.rmtree('test/temp-data')
        shutil.rmtree('test/results-data')

    def test_file_exist_after_mem_compand(self):
        """
        Try to compress to an in-memory tarball storing test folder structure as a rerooted structure.
        then expand again in a different destination folder. 
        Apply a filter on archived files: take only .txt files. In fact skip ignore.tx"""
        memory = io.BytesIO()
        
        instruction = pony.pack('test/temp-data', 'test-data', '*.txt')
        pony.gz_package(package_instructions= [instruction], mem=memory)
        
        memory = io.BytesIO(memory.getvalue())
        instruction = pony.unpack('test-data', 'test/results-data')
        pony.gz_unbox(unbox_instructions= [instruction], mem = memory)
        
        
        self.assertTrue (os.path.exists('test/results-data/one.txt'))
        self.assertTrue (os.path.exists('test/results-data/two.txt'))
        self.assertTrue (os.path.exists('test/results-data/subfolder/three.txt'))
        self.assertTrue (os.path.exists('test/results-data/subfolder/subsubfolder/four.txt'))
        
        self.assertFalse(os.path.exists('test/results-data/subfolder/ignore.tx'))

    def test_complex_archiving_rerooting(self):
        """
        Tests the compand operation when source folder structure is reorganized in a complex way.
        Some subfolder into different level folders. """
        memory = io.BytesIO()
        
        instructions = [ 
                        pony.pack('test/temp-data', 'test-data', '*.txt'),
                        pony.pack('test/temp-data/subfolder/subsubfolder', 'moved-folder', '*.txt')
                      ]
                  
        pony.gz_package(package_instructions= instructions, mem=memory)
        
        memory = io.BytesIO(memory.getvalue())
        instructions = [
                        pony.unpack('test-data', 'test/results-data'),
                        pony.unpack('moved-folder', 'test/results-data')
                       ]
        pony.gz_unbox(unbox_instructions= instructions, mem = memory)
        
        
        self.assertTrue (os.path.exists('test/results-data/one.txt'))
        self.assertTrue (os.path.exists('test/results-data/two.txt'))
        self.assertTrue (os.path.exists('test/results-data/subfolder/three.txt'))
        self.assertTrue (os.path.exists('test/results-data/four.txt'))
        
        # it also has not extracted the rerooted elements into their original structure
        self.assertFalse (os.path.exists('test/results-data/subfolder/subsubfolder/four.txt'))
        self.assertFalse(os.path.exists('test/results-data/subfolder/ignore.tx'))
        
if __name__ == '__main__':
    unittest.main()