import unittest
import cli
import bag 
from test.facilities import *
import shutil

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        """
        Setup multiple (but minimal) projects and their dependencies.

        +-----+         +-----+             +-----+         +-----+
        | Av0 | ------->| Bv1 | ----------->| Cv1 | ------->| Dv1 |
        +-----+         +-----+             +-----+         +-----+
           |                                   |
           |            +-----+                |         +-----+
           |            |     |                +-------->|     |
           +----------->| Bv2 |------------------------->| Dv2 |
           |            |     |---------------+  +------>|     |
           |            +-----+               |  |       +-----+
           |                                  v  |
           |            +-----+             +-------+       +-----+
           +----------->| Bv3 | ----------->| Cv2   |------>| Dv3 |
                        +-----+             +-------+       +-----+
        
        
        Each of these projects contains only one file named test_<project-name>_v<version>
        and only two real metadata NAME and VERSION plus a tag to erase them  from the server once 
        the tests are done (TEST).
        """

        mongo_clean()
        projects =  {"A": [0], "B": [1,2,3], "C":[1,2], "D": [1,2,3] }
        metainfo = {"A": {}, "B": {}, "C":{}, "D": {} }
# prepare metainformations for Av0
        metainfo["A"][0] = """
{
    "NAME" : "A",
    "VERSION" : "0",
    "TEST" : "",

    "DEPENDENCIES" : [
        {
            "NAME" : "B",
            "VERSION" : { "$lte": "3",  "$gte" : "1" }
        }
    ],
    
    "__BOX_INSTRUCTIONS__" : [
                        {
                            "FROM" 		: "", 
                            "TO" 		: "package-folder", 
                            "FILTER" 	: "*"
                        }
    ],

    "__UNBOX_INSTRUCTIONS__" : [
                        {
                            "FROM" 		: "package-folder", 
                            "TO" 		: "result-folder", 
                            "FILTER" 	: "*"
                        }
    ]

}""" 

        metainfo["B"][1] = """
{
    "NAME" : "B",
    "VERSION" : "1",
    "TEST": "",

    "DEPENDENCIES" : [
        {
            "NAME" : "C",
            "VERSION" : "1" 
        } 
    ],
    
    "__BOX_INSTRUCTIONS__" : [
                        {
                            "FROM" 		: "", 
                            "TO" 		: "package-folder", 
                            "FILTER"   : "*.file" 
                        }
    ],

    "__UNBOX_INSTRUCTIONS__" : [
                        {
                            "FROM" 		: "package-folder", 
                            "TO" 		: "result-folder", 
                            "FILTER"   : "*.file"
                        }
    ]

}"""


        metainfo["B"][2] = """
{
    "NAME" : "B",
    "VERSION" : "2",
    "TEST": "",

    "DEPENDENCIES" : [
        {
            "NAME" : "D",
            "VERSION" : "2" 
        },
        
        {
            "NAME" : "C",
            "VERSION" : "2" 
        } 
    ],
    
    "__BOX_INSTRUCTIONS__" : [
                        {
                            "FROM" 		: "", 
                            "TO" 		: "package-folder", 
                            "FILTER"   : "*.file"   
                        }
    ],

    "__UNBOX_INSTRUCTIONS__" : [
                        {
                            "FROM" 		: "package-folder", 
                            "TO" 		: "result-folder", 
                            "FILTER"   : "*.file"   
                        }
    ]

}"""

        metainfo["B"][3] = """
{
    "NAME" : "B",
    "VERSION" : "3",
    "TEST": "",

    "DEPENDENCIES" : [
        {
            "NAME" : "C",
            "VERSION" : "2" 
        } 
    ],
    
    "__BOX_INSTRUCTIONS__" : [
                        {
                            "FROM" 		: "", 
                            "TO" 		: "package-folder", 
                            "FILTER"   : "*.file"   
                        }
    ],

    "__UNBOX_INSTRUCTIONS__" : [
                        {
                            "FROM" 		: "package-folder", 
                            "TO" 		: "result-folder", 
                            "FILTER"   : "*.file"   
                        }
    ]

}"""

        metainfo["C"][1] = """
{
    "NAME" : "C",
    "VERSION" : "1",
    "TEST": "",

    "DEPENDENCIES" : [
        {
            "NAME" : "D",
            "VERSION" : { "$lte": "2",  "$gte" : "1" } 
        }
    ],
    
    "__BOX_INSTRUCTIONS__" : [
                        {
                            "FROM" 		: "", 
                            "TO" 		: "package-folder", 
                            "FILTER"   : "*.file"   
                        }
    ],

    "__UNBOX_INSTRUCTIONS__" : [
                        {
                            "FROM" 		: "package-folder", 
                            "TO" 		: "result-folder", 
                            "FILTER"   : "*.file"   
                        }
    ]

}"""

        metainfo["C"][2] = """
{
    "NAME" : "C",
    "VERSION" : "2",
    "TEST": "",

    "DEPENDENCIES" : [
        {
            "NAME" : "D",
            "VERSION" : "3"
        }
    ],
    
    "__BOX_INSTRUCTIONS__" : [
                        {
                            "FROM" 		: "", 
                            "TO" 		: "package-folder", 
                            "FILTER"   : "*.file"   
                        }
    ],

    "__UNBOX_INSTRUCTIONS__" : [
                        {
                            "FROM" 		: "package-folder", 
                            "TO" 		: "result-folder", 
                            "FILTER"   : "*.file"   
                        }
    ]

}"""

        metainfo["D"][1] = """
{
    "NAME" : "D",
    "VERSION" : "1",
    "TEST": "",
    
    "__BOX_INSTRUCTIONS__" : [
                        {
                            "FROM" 		: "", 
                            "TO" 		: "package-folder", 
                            "FILTER"   : "*.file"   
                        }
    ],

    "__UNBOX_INSTRUCTIONS__" : [
                        {
                            "FROM" 		: "package-folder", 
                            "TO" 		: "result-folder", 
                            "FILTER"   : "*.file"   
                        }
    ]

}"""

        metainfo["D"][2] = """
{
    "NAME" : "D",
    "VERSION" : "2",
    "TEST": "",

    "DEPENDENCIES" : [
    ],
    
    "__BOX_INSTRUCTIONS__" : [
                        {
                            "FROM" 		: "", 
                            "TO" 		: "package-folder", 
                            "FILTER"   : "*.file"   
                        }
    ],

    "__UNBOX_INSTRUCTIONS__" : [
                        {
                            "FROM" 		: "package-folder", 
                            "TO" 		: "result-folder", 
                            "FILTER"   : "*.file"   
                        }
    ]

}"""

        metainfo["D"][3] = """
{
    "NAME" : "D",
    "VERSION" : "3",
    "TEST": "",
    
    "__BOX_INSTRUCTIONS__" : [
                        {
                            "FROM" 		: "", 
                            "TO" 		: "package-folder", 
                            "FILTER"   : "*.file"   
                        }
    ],

    "__UNBOX_INSTRUCTIONS__" : [
                        {
                            "FROM" 		: "package-folder", 
                            "TO" 		: "result-folder", 
                            "FILTER"   : "*.file"   
                        }
    ]

}"""

        for p in projects:
            versions = projects[p]
            for v in versions:
                folder = "test/test-cli/test-projects/" + p +"v" + str(v)
                project_file = folder + "/test_" + p +"_v" + str(v) + ".file"
                ensure_path(folder)
                touch(project_file)

                with open(folder + "/meta.json", "w") as f:
                    f.write(metainfo[p][v])
                    
                self._store_project_at(folder)

    def tearDown(self):
        """
        Destroy temporary folder structure and remove any mongo documents (pony box) 
        inserted temporary for test purpose
        """
        shutil.rmtree('test/test-cli')
        mongo_clean()

    def _store_project_at(self, folder):
        # set the current working directory to the project folder to mimic
        # the common use case
        restore_cwd = os.getcwd()

        os.chdir(folder)
        command_line = "pony charge".split(' ')
        arguments = cli.parser.parse_args(command_line[1:])
        arguments.func(arguments)

        # restore the original cwd
        os.chdir(restore_cwd)

    def test_cli_store_op(self):
        """
        Checks projects have been stored during the setup fase with the correct (basic) meta informations
        given into meta.json files
        """

        with MongoChecker() as ck:
            self.assertTrue(ck.contain({"NAME" : "A", "VERSION" : "0"}))
            self.assertTrue(ck.contain({"NAME" : "B", "VERSION" : "1"}))
            self.assertTrue(ck.contain({"NAME" : "B", "VERSION" : "2"}))
            self.assertTrue(ck.contain({"NAME" : "B", "VERSION" : "3"}))
            self.assertTrue(ck.contain({"NAME" : "C", "VERSION" : "1"}))
            self.assertTrue(ck.contain({"NAME" : "C", "VERSION" : "2"}))
            self.assertTrue(ck.contain({"NAME" : "D", "VERSION" : "1"}))
            self.assertTrue(ck.contain({"NAME" : "D", "VERSION" : "2"}))
            self.assertTrue(ck.contain({"NAME" : "D", "VERSION" : "3"}))

    def test_cli_deliver_op_no_dep(self):
        """
        Checks the deliver operation requested to build projects without
        extra dependencies (projects named D in the example).

        The only file added after a deliver operation on this kind of projects should be 
        .pony, the one that lists files from other projects
        """

        with WorkingDirectorySet("test/test-cli/test-projects/Dv1") as project_folder:
            command_line = "pony deliver".split(' ')
            arguments = cli.parser.parse_args(command_line[1:])
            arguments.func(arguments)

            prj_folder_files = files_in()
            prj_subfolders = subfolders_in()
            self.assertEqual(3, len(prj_folder_files), msg="more files then expected in project folder they are: " + str(prj_folder_files) )
            self.assertEqual(0, len(prj_subfolders), msg="created new folders after deliver operation they are: " + str(prj_subfolders) )

    def test_cli_deliver_op_simple_dep(self):
        """
        Checks the deliver operation required to build simple projects with only one
        dependency and no alternatives, successfully prepare the project environment
        Will use Cv2 witch depends only on Dv3 or Dv2 as an example project.

        This test also checks that dependencies are stored on mongo collection the 
        proper way during store operation
        """

        with WorkingDirectorySet("test/test-cli/test-projects/Cv2") as project_folder:
            command_line = "pony deliver".split(' ')
            arguments = cli.parser.parse_args(command_line[1:])
            arguments.func(arguments)

            prj_folders_files = files_in()
            prj_subfolders = subfolders_in()

            self.assertEqual(3, len(prj_folders_files), msg="Expect no new file other then .pony created in project folder. File list actually is: " + str(prj_folders_files) )
            self.assertEqual(1, len(prj_subfolders), msg="Expected result-folder created as project root folder subdirectory given the __UNBOX_INSTRUCTION__ into project metadata. Subfolders are: " + str(prj_subfolders) )
            self.assertEqual("result-folder", prj_subfolders[0], msg="Expect the only project subfolder created to be result-folder" )
            self.assertEqual(1, len(files_in('result-folder')), msg="Expect one new file created in result-folder.File list actually is: " + str('result-folder') ) 

    def test_cli_deliver_op_simple_transitive_dep(self):
        """
        Checks the deliver operation when required to build projects with transitive dependencies.

        Here I'll use Bv1 which depends on Cv1 and in turn on Dv1 or Dv2 alternativelly. This will check pony detect and resolve
        correctly indirect dependencies. Still no constraing is required apart of dependency tree arbitrary pruning on alternatives.
        """

        with WorkingDirectorySet("test/test-cli/test-projects/Bv1"):
            command_line = "pony deliver".split(' ')
            arguments = cli.parser.parse_args(command_line[1:])
            file_list, gr = arguments.func(arguments)

            prj_folders_files = files_in()
            prj_subfolders = subfolders_in()

            self.assertEqual(bag.to_dot_string(gr), """digraph {
    "{ NAME:C, VERSION:1 }" [penwidth=3 ];
    "{ NAME:D, VERSION:1 }" [penwidth=3 color=blue ];
    "{ NAME:D, VERSION:2 }" [penwidth=3 ];

    "{ NAME:C, VERSION:1 }" -> "{ NAME:D, VERSION:1 }"[color=black penwidth=3];
    "{ NAME:C, VERSION:1 }" -> "{ NAME:D, VERSION:2 }"[color=black penwidth=3];
}
"""
            )

            self.assertEqual(3, len(prj_folders_files), 
                                msg="Expect no new file other then .pony created in project folder. File list actually is: " + str(prj_folders_files) )
            self.assertEqual(1, len(prj_subfolders),
                                msg="Expected result-folder created as project root folder subdirectory given the __UNBOX_INSTRUCTION__ into project metadata. Subfolders are: " + str(prj_subfolders) )
            self.assertEqual("result-folder", prj_subfolders[0],
                                msg="Expect the only project subfolder created to be result-folder" )
            self.assertEqual(2, len(files_in(folder="result-folder")), 
                                msg="Expect exactly 2 files created into the dependency destination folder, one for each projects. File list actually is: " + str(os.listdir("result-folder")) )
             

    def test_cli_deliver_op_complex_transitive_dep(self):
        """
        Checks the deliver operation when required to build projects with complex transitive dependencies.

        Here pony is supposed to use constraints to resolve dependencies that can
        fulfill all transitive dependencies. 

        I'll use Av0 the dependency graph can be seen as documentation of setup method.
        """

        with WorkingDirectorySet("test/test-cli/test-projects/Av0"):
            command_line = "pony deliver".split(' ')
            arguments = cli.parser.parse_args(command_line[1:])
            try:
                file_list, gr = arguments.func(arguments)
            except  bag.TransitiveDependencyUnreachable as e:
                print ("EXCEPTION EXCEPTION")
                print (bag.to_dot_string(e.gr))
                raise e


            prj_folders_files = files_in()
            prj_subfolders = subfolders_in()
            self.maxDiff = None
            result_graph = bag.to_dot_string(gr)
            self.assertEqual(result_graph, """digraph {
    "{ NAME:B, VERSION:1 }" [penwidth=3 color=blue ];
    "{ NAME:B, VERSION:2 }" [penwidth=3 color=blue ];
    "{ NAME:B, VERSION:3 }" [penwidth=3 ];
    "{ NAME:C, VERSION:1 }" [penwidth=3 color=blue ];
    "{ NAME:C, VERSION:2 }" [penwidth=3 ];
    "{ NAME:D, VERSION:1 }" [penwidth=3 color=blue ];
    "{ NAME:D, VERSION:2 }" [penwidth=3 color=blue ];
    "{ NAME:D, VERSION:3 }" [penwidth=3 ];

    "{ NAME:B, VERSION:1 }" -> "{ NAME:C, VERSION:1 }"[color=black penwidth=3];
    "{ NAME:B, VERSION:2 }" -> "{ NAME:C, VERSION:2 }"[color=black penwidth=3];
    "{ NAME:B, VERSION:2 }" -> "{ NAME:D, VERSION:2 }"[color=black penwidth=3];
    "{ NAME:B, VERSION:3 }" -> "{ NAME:C, VERSION:2 }"[color=black penwidth=3];
    "{ NAME:C, VERSION:1 }" -> "{ NAME:D, VERSION:1 }"[color=black penwidth=3];
    "{ NAME:C, VERSION:1 }" -> "{ NAME:D, VERSION:2 }"[color=black penwidth=3];
    "{ NAME:C, VERSION:2 }" -> "{ NAME:D, VERSION:3 }"[color=black penwidth=3];
}
"""
            )

            self.assertEqual(3, len(prj_folders_files), 
                                msg="Expect no new file other then .pony created in project folder. File list actually is: " + str(prj_folders_files) )
            self.assertEqual(1, len(prj_subfolders),
                                msg="Expected result-folder created as project root folder subdirectory given the __UNBOX_INSTRUCTION__ into project metadata. Subfolders are: " + str(prj_subfolders) )
            self.assertEqual("result-folder", prj_subfolders[0],
                                msg="Expect the only project subfolder created to be result-folder" )
            self.assertEqual(3, len(files_in(folder="result-folder")), 
                                msg="Expect exactly 3 files created into the dependency destination folder, one for each projects it depends from. File list actually is: " + str(os.listdir("result-folder")) )
             

        



        


