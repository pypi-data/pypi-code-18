#!python3

import unittest
import shutil
import os


import pymongo
import pony
from bag import to_dot_string


def ensure_path(path):
    """ensure the full path received exists"""
    try:
        os.makedirs(path)
    except FileExistsError:
        pass

def touch(file_path):
    """create an empty file at the specified path"""
    tempf = open(file_path, 'w')
    tempf.close()


def touch_some_files():
    """Create an input folder structure"""
    print('setting up')
    ensure_path('test/temp-data/subfolder/subsubfolder')
    touch('test/temp-data/one.txt')
    touch('test/temp-data/two.txt')
    touch('test/temp-data/subfolder/ignore.tx')
    touch('test/temp-data/subfolder/three.txt')
    touch('test/temp-data/subfolder/subsubfolder/four.txt')

def erase_temp_files():
    """Destroy temporary folder structure"""
    shutil.rmtree('test/temp-data')

class TestMongoStoreOp(unittest.TestCase):
    """Test the store operation on real mongo db"""

    def setUp(self):
        touch_some_files()

    def tearDown(self):
        """Destroy temporary folder structure"""
        erase_temp_files()

        connection = pymongo.MongoClient('localhost', 27017)
        db = connection.pony_store
        collection = db.packages

        collection.delete_many({"name" : "temp"})


    def test_save_package_and_metadata_in_mongo(self):
        """
        Checks both 'raw' package data and related metadata are correctly stored in mongo db.
        This also checks you cannot store multiple time projects with same metadata.
        """
        # establish mongo connection and retrieve the pony_store collection
        connection = pymongo.MongoClient('localhost', 27017)
        collection = connection.pony_store.packages

        # prepare some packaging instructions and metadata
        instructions = [
            pony.pack(
                'test/temp-data',
                'test-data',
                '*.txt'
            ),
            pony.pack(
                'test/temp-data/subfolder/subsubfolder',
                'moved-folder',
                '*.txt'
            )
        ]

        some_metadata = {"name" : "temp", "version" : "0.1.3", "target" : "x86"}

        # clean the collection from any document with same (test) metadata
        collection.delete_many(some_metadata)
        pony.charge(instructions, some_metadata)

        # checks mongo has a correspondant document stored!
        package = collection.find({"name" : "temp", "version" : "0.1.3", "target" : "x86"})
        self.assertTrue(package[0]['package'])

        # and that it prevent you from store multiple artifact with same metadata!
        with self.assertRaises(pony.bag.YetInBag):
            pony.charge(instructions, some_metadata)

    def test_save_package_and_complex_metadata(self):
        """
        Checks both 'raw' package data and related metadata are correctly stored in mongo db.
        (more complex metadata: complex dependency specified).
        This also checks you cannot store multiple time projects with same metadata but different
        dependencies.
        """
        # establish mongo connection and retrieve the pony_store collection
        connection = pymongo.MongoClient('localhost', 27017)
        collection = connection.pony_store.packages

        # prepare some packaging instructions and metadata
        instructions = [
            pony.pack(
                'test/temp-data',
                'test-data',
                '*.txt'
            ),
            pony.pack(
                'test/temp-data/subfolder/subsubfolder',
                'moved-folder',
                '*.txt'
            )
        ]

        some_metadata = {
            "name" : "temp",
            "version" : "0.1.4",
            "target" : "x86",
            "DEPENDENCIES" : [
                {
                    "NAME" : "A_PROJECT",
                    "VERSION" : {"$gte" : "0.0.1"}
                }
            ]
        }

        # clean the collection from any document with same (test) metadata
        collection.delete_many(some_metadata)
        pony.charge(instructions, some_metadata)

        # checks mongo has a correspondant document stored!
        package = collection.find({"name" : "temp", "version" : "0.1.4", "target" : "x86"})
        self.assertTrue(package[0]['package'])

        # and that it prevent you from store multiple artifact with same metadata!
        with self.assertRaises(pony.bag.YetInBag):
            pony.charge(instructions, some_metadata)

    def test_insert_based_on_json(self):
        """
        Checks pony charge a box completelly described by mean of json string and by
        boxing instructions referring to files on the filesyste.
        """
        # establish mongo connection and retrieve the pony_store collection
        connection = pymongo.MongoClient('localhost', 27017)
        collection = connection.pony_store.packages

        pony.charge(json="""
        {
            "name"    : "temp", 
            "version" : "0.1.3", 
            "target"  : "x86",
            
           "__BOX_INSTRUCTIONS__" : [
                                    {
                                        "FROM"      : "test/temp-data", 
                                        "TO"        : "test-data", 
                                        "FILTER"    : "*.txt"
                                    },
                                    {
                                        "FROM"      : "test/temp-data/subfolder/subsubfolder", 
                                        "TO"        : "moved-folder", 
                                        "FILTER"    : "*.txt"
                                    }
            ]
        }
        """)

        # checks mongo has a correspondant document stored!
        package = collection.find({"name" : "temp", "version" : "0.1.3", "target" : "x86"})
        self.assertTrue(package[0]['package'])

    def test_insert_based_on_json_file(self):
        """
        Checks pony charge a box completelly described by mean of json file and by
        boxing instructions referring to files on the filesystem.
        """
        # establish mongo connection and retrieve the pony_store collection
        connection = pymongo.MongoClient('localhost', 27017)
        collection = connection.pony_store.packages

        json_content = """
        {
            "name" : "temp", 
            "version" : "0.1.3", 
            "target" : "x86",
            
           "__BOX_INSTRUCTIONS__" : [
                                    {
                                        "FROM"      : "test/temp-data", 
                                        "TO"        : "test-data", 
                                        "FILTER"    : "*.txt"
                                    },
                                    {
                                        "FROM"      : "test/temp-data/subfolder/subsubfolder", 
                                        "TO"        : "moved-folder", 
                                        "FILTER"    : "*.txt"
                                    }
            ]
        }
        """
        with open("temp.json", "w") as out_file:
            out_file.write(json_content)

        pony.charge(file="temp.json")
        # checks mongo has a correspondant document stored!
        package = collection.find({"name" : "temp", "version" : "0.1.3", "target" : "x86"})
        self.assertTrue(package[0]['package'])

class TestMongoMetarequestQuery(unittest.TestCase):
    def setUp(self):
        pony.silent = True
        touch_some_files()
        self.connection = pymongo.MongoClient('localhost', 27017)
        self.collection = self.connection.pony_store.packages

        instructions = [
            pony.pack('test/temp-data', 'test-data', '*.txt'),
            pony.pack('test/temp-data/subfolder/subsubfolder', 'moved-folder', '*.txt')
        ]

        self.collection.delete_many(
            {"NAME" : "dep-v1"}
        )
        self.collection.delete_many(
            {"NAME" : "prj61"}
        )

        meta = {"NAME" : "dep-v1",
                "VERSION" : "1.0.0"}
        pony.charge(instructions, meta)

        meta = {"NAME" : "dep-v1",
                "VERSION" : "0.1.0"}
        pony.charge(instructions, meta)

        meta = {"NAME" : "prj61",
                "VERSION" : "1.3.0"}

        pony.charge(instructions, meta)

        meta = {"NAME" : "dep-v1",
                "VERSION" : "1.1.0"}
        pony.charge(instructions, meta)

    def tearDown(self):
        pony.silent = True
        erase_temp_files()
        #also erase files created as results
        try:
            shutil.rmtree('test/results-data')
        except FileNotFoundError:
            pass
        self.collection.delete_many(
            {"NAME" : "dep-v1"}
        )
        self.collection.delete_many(
            {"NAME" : "prj61"}
        )
        self.connection.close()

    def test_deliver_op_version_exact(self):
        """
        Test a ssuccess case, it must successfully
        unbox a stored package with request metadata
        """

        instructions = [
            pony.unpack('test-data', 'test/results-data'),
            pony.unpack('moved-folder', 'test/results-data')
        ]

        meta_request = {"NAME" : "dep-v1", "VERSION" :  "1.0.0"}
        pony.deliver(instructions, meta_request)

        self.assertTrue(
            os.path.exists('test/results-data/one.txt')
        )
        self.assertTrue(
            os.path.exists('test/results-data/two.txt')
        )
        self.assertTrue(
            os.path.exists('test/results-data/subfolder/three.txt')
        )

    def test_deliver_op_return_created_files(self):
        """
        Test a ssuccess case, it must successfully unbox a stored package
        with request metadata
        """

        instructions = [
            pony.unpack('test-data', 'test/results-data'),
            pony.unpack('moved-folder', 'test/results-data')
        ]
        meta_request = {"NAME" : "prj61", "VERSION" :  "1.3.0"}
        created_files, dep_graph = pony.deliver(instructions, meta_request)

        for fname in ['test/results-data/one.txt', 'test/results-data/two.txt', 'test/results-data/subfolder/three.txt']:
            self.assertTrue(
                fname in created_files,
                msg = str(fname) + ' not in '+ str(created_files) + '\nDependency graph is\n' + to_dot_string(dep_graph)
            )

    def test_deliver_op_version_greater(self):
        """
        Test a success case, it must successfully unbox a stored package
        with request metadata (version greater then)
        """

        instructions = [
            pony.unpack('test-data', 'test/results-data'),
            pony.unpack('moved-folder', 'test/results-data')
        ]

        meta_request = {"NAME" : "dep-v1", "VERSION" : {"$gte" : "0.9.0"}}
        pony.deliver(instructions, meta_request)

        self.assertTrue(
            os.path.exists('test/results-data/one.txt')
        )
        self.assertTrue(
            os.path.exists('test/results-data/two.txt')
        )
        self.assertTrue(
            os.path.exists('test/results-data/subfolder/three.txt')
        )

    def test_deliver_op_fail_version_exact(self):
        """
        Test a fail case, it must raise NotInBag exception because
        there isn't a stored package with request metadata
        """

        instructions = [
            pony.unpack('test-data', 'test/results-data'),
            pony.unpack('moved-folder', 'test/results-data')
        ]

        meta_request = {"NAME" : "dep-v1", "VERSION" :  "1.0.1"}
        with self.assertRaises(pony.bag.NotInBag):
            pony.deliver(instructions, meta_request)

    def test_deliver_op_version_greater_from_json(self):
        """
        Checks pony can deliver boxes based on json a requirement
        description (actually just a single requirement description)
        and the instructions for the unboxing.
        In this case the requireiment description is complex, it is like: version greater then...
        """
        import json
        json_string = """
        [
                {"NAME" : "dep-v1", "VERSION" :  {"$gte" : "0.9.0"} }
        ]"""
        meta_request = json.loads(json_string)

        instructions = [
            pony.unpack('test-data', 'test/results-data'),
            pony.unpack('moved-folder', 'test/results-data')
        ]

        requirements, gr = pony.deliver(instructions, meta_request[0])
        instructions = [
            pony.pack(
                'test/temp-data',
                'test-data',
                '*.txt'
            ),
            pony.pack(
                'test/temp-data/subfolder/subsubfolder',
                'moved-folder',
                '*.txt'
            )
        ]
        self.assertTrue(
            os.path.exists('test/results-data/one.txt')
        )
        self.assertTrue(
            os.path.exists('test/results-data/two.txt')
        )
        self.assertTrue(
            os.path.exists('test/results-data/subfolder/three.txt')
        )

        # checks the log from the deliver operation. This will check the all compatible versions of dependencies are taken into account
        # and that only one is seleceted to resolve dependency. 

        self.assertEqual("""digraph {
    "{ NAME:dep-v1, VERSION:1.0.0 }" [penwidth=3 color=blue ];
    "{ NAME:dep-v1, VERSION:1.1.0 }" [penwidth=3 ];

}
""" , to_dot_string(gr), msg=to_dot_string(gr))


    def test_deliver_op_version_greater_from_simple_and_complete(self):
        """
        Checks pony can deliver boxes based on json description of project metadata:
            - metadata strictly concerning the project
            - dependency metadata
            - unbox instructions
        In this case the requreiment description is complex, it is like: version greater then...
        """

        import json
        json_string = """
        {
            "NAME" : "TEST",
            "DEPENDENCIES" :
                            [
                                {"NAME" : "dep-v1", "VERSION" :  {"$gte" : "0.9.0"} }

                            ],

            "__UNBOX_INSTRUCTIONS__" : [
                 {
                    "FROM" : "test-data", 
                    "TO"   :  "test/results-data",
                    "FILTER" : "*"
                 },
                 {
                    "FROM" :  "moved-folder", 
                    "TO"   :  "test/results-data",
                    "FILTER" : "*"
                 }
            ]

        }"""

        pony.deliver_json(json_string)

        self.assertTrue(
            os.path.exists('test/results-data/one.txt')
        )
        self.assertTrue(
            os.path.exists('test/results-data/two.txt')
        )
        self.assertTrue(
            os.path.exists('test/results-data/subfolder/three.txt')
        )

    def test_deliver_op_multiple_dependencies(self):
        """
        Checks can retrieve multiple dependencies using only one set of unpack instructions.

        Checks pony can deliver boxes based on json description of project dependencies metadata:
            - dependency metadata
            - unbox instructions

        In this case the requreiment description is complex, it is like: version greater then...
        In this case there are multiple acceptable dependency project version. Pony shall
        chose any of those and success.

        Checks also that the requirement graph constructed from json dependency description, is the same as the one contructed
        based on lower level dependency description (by means of python objects). 

        
        """

        import json
        json_string = """
        [
                {   "NAME" :  "dep-v1",
                    "VERSION" :  {"$gte" : "0.9.0"} 
                },

                {   "NAME"      : "prj61",
                    "VERSION"   : "1.3.0"
                }
        ]"""

        # construct the requirement description object from json and from python object.
        meta_request = json.loads(json_string)
        meta_request_raw = [{"NAME" : "dep-v1", "VERSION" : {"$gte" : "0.9.0"}}, {"NAME" : "prj61", "VERSION" : "1.3.0"}] 

        instructions = [
            pony.unpack('test-data', 'test/results-data'),
            pony.unpack('moved-folder', 'test/results-data')
        ]

        # ask pony to deliver dependencies as described from the requirements constructed from json and from raw python object.
        files, gr = pony.deliver(instructions, meta_request)
        files_raw, gr_raw = pony.deliver(instructions, meta_request_raw)

        fail_message = "The requirement graph constructed from json string is:\n" + to_dot_string(gr) + "\nwhile the one constructed from equivalent python object is:\n" + to_dot_string(gr_raw)
        self.assertEqual( to_dot_string(gr), to_dot_string(gr_raw), msg= fail_message )

        self.assertTrue(
            os.path.exists('test/results-data/one.txt')
        )
        self.assertTrue(
            os.path.exists('test/results-data/two.txt')
        )
        self.assertTrue(
            os.path.exists('test/results-data/subfolder/three.txt')
        )

    def test_pony_report_chosed_dependencies_as_networkx_graph(self):
        """
        The deliver operation return as a result the list of created
        files as a result of the dependency resolution process
        It also must produce a log of the dependency resolution process
        in the form of a networkx graph.
        """

        import json
        encoded_string = """
        {
            "NAME" : "TEST",
            "DEPENDENCIES" :
                            [
                                {"NAME" : "dep-v1", "VERSION" :  {"$gte" : "0.9.0"} }

                            ],

            "__UNBOX_INSTRUCTIONS__" : [
                 {
                    "FROM" : "test-data", 
                    "TO"   :  "test/results-data",
                    "FILTER" : "*"
                 },
                 {
                    "FROM" :  "moved-folder", 
                    "TO"   :  "test/results-data",
                    "FILTER" : "*"
                 }
            ]

        }"""

        file_list, gr = pony.deliver_json(encoded_string)

        self.assertEqual("""digraph {
    "{ NAME:dep-v1, VERSION:1.0.0 }" [penwidth=3 color=blue ];
    "{ NAME:dep-v1, VERSION:1.1.0 }" [penwidth=3 ];

}
""" , to_dot_string(gr), msg=to_dot_string(gr))


if __name__ == '__main__':
    unittest.main()
    