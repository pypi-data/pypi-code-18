import unittest
import collections
import dependencies as dep
import bag 
from bag import Bag, to_dot_string
import networkx as nx
import time
from operator import xor


class TestRequirementFunctionalities (unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def test_can_construct_requirement_using_dict (self):
    """
    """
    
    req = dep.Requirement ( { 
                              "NAME" : "DEP-1",
                              "VERSION" : "1.1.1"
                            }
    )
    
    self.assertTrue( hasattr(req, "NAME") )
    self.assertEqual( req.NAME, "DEP-1")
    
    self.assertTrue( hasattr(req, "VERSION") )
    self.assertEqual( req.VERSION,  "1.1.1") 
    
    
  def test_requirements_equal_on_lose_match(self):
    req1 = dep.Requirement ( { 
                              "NAME" : "DEP-1",
                              "VERSION" : "1.0.1"
                            }
    )
    
    req2 = dep.Requirement ( { 
                              "NAME" : "DEP-1",
                              "VERSION" : "1.1.1"
                            }
    )
    
    req_match_1 = dep.Requirement ( { 
                              "NAME" : "DEP-1",
                              "VERSION" : "1.0.1"
                            }
    )
    
    self.assertTrue(req1.alternative(req2))
    self.assertFalse(req1.perfect_match(req2))
    self.assertEqual(req1, req_match_1)
    self.assertTrue(req1, req_match_1)
    
    
  def test_direct_dependencies_extraction(self):
    """
    pony can receive a metainformation object and build direct requirements.
    The metainformations object can be constructed by decoding a json string into a python object the default way.
    """
    direct_dependencies = dep.make_direct(  [
                                              {
                                                "NAME" : "DEP-1",
                                                "VERSION" : "1.1.1"
                                              },
                                              {
                                                "NAME" : "DEP-2",
                                                "VERSION" : "1.2.3"
                                              }
                                            ]
    )
    
    # construct the collection of expected objects to check for match
    expected_objects = [
                        dep.Requirement( {
                                        "NAME" : "DEP-1",
                                        "VERSION" : "1.1.1"
                        }),
                                      
                        dep.Requirement( {
                                        "NAME" : "DEP-1",
                                        "VERSION" : "1.1.1"
                        })
                        ]
    
    # direct_dependencies is an iterable object
    self.assertTrue( isinstance(direct_dependencies, collections.Iterable) )
    # it contains exactly two elements
    self.assertEqual( len(direct_dependencies), 2)
    # it contains all the expected objects
    for expected in expected_objects:
      self.assertTrue(expected in direct_dependencies) 
  
  def test_can_represent_dependency_graph_using_dot(self):  
    r1 = dep.Requirement( {"NAME" : "DEP-1", "VERSION" : "1.1.1"} )   
    r2 = dep.Requirement( { "NAME" : "DEP-2", "VERSION" : "1.0.1" })
    
    r2_1= dep.Requirement( { "NAME" : "DEP-2-1", "VERSION" : "1.0.1" })
    r2_1.parent = r2
    r2_2= dep.Requirement( { "NAME" : "DEP-2-2", "VERSION" : "1.0.6" })
    r2_2.parent = r2
    
    
    r2_1_1= dep.Requirement( { "NAME" : "DEP-2-1-1", "VERSION" : "1.0.6" })
    r2_1_1.parent = r2_1
    
    dot_graph = dep.dot_graph([r1, r2, r2_1, r2_2, r2_1_1])
    self.assertEqual(dot_graph, """
digraph {
  "DEP-1"
  "DEP-2"

  "DEP-2-1" -> "DEP-2"
  "DEP-2-2" -> "DEP-2"
  "DEP-2-1-1" -> "DEP-2-1"
}""")
    print("DOT:  "+ dot_graph)
      

class TestBagRequirementDiscover (unittest.TestCase):
  def setUp(self):
    self.connected_bag = Bag()
    self.connected_bag.silent = True;
    repo = self.connected_bag
    repo.collection.delete_many({"TEST" : ""})
    self.dep_1 = {"NAME" : "DEP-1", "VERSION" : "0.1.0", "TEST" : ""}
    self.dep_2 = {"NAME" : "DEP-2", "VERSION" : "0.1.0", "TEST" : "", 
                      "DEPENDENCIES" : [ 
                                        {"NAME" : "DEP-2-1", "VERSION" : "1.1.1"},
                                        {"NAME" : "DEP-2-2", "VERSION" : "1.2.3"}
                                       ] }
    repo.charge(None, self.dep_1 )
    repo.charge(None, {"NAME" : "DEP-2-1", "VERSION" : "1.1.1", "TEST" : ""} )
    repo.charge(None, {"NAME" : "DEP-2-2", "VERSION" : "1.2.3", "TEST" : ""} )
    repo.charge(None,  self.dep_2 )    
    repo.charge(None, {"NAME" : "P1", "VERSION" : "1.0.0", "TEST" : "", 
                      "DEPENDENCIES" : [ 
                                        {"NAME" : "DEP-1", "VERSION" : "0.1.0"},
                                        {"NAME" : "DEP-2", "VERSION" : "0.1.0"}
                                       ] } )

    repo.charge(None, {"NAME" : "P0", "VERSION" : "1.0.0", "TEST" : "", 
                      "DEPENDENCIES" : [ 
                                        {"NAME" : "DEP-1", "VERSION" : "0.1.0"},
                                        {"NAME" : "DEP-2-1", "VERSION" : "1.1.1", "TEST" : ""}
                                       ] } )
    
    self.connected_bag.silent = False;

  def tearDown(self):
    self.connected_bag.collection.delete_many({"TEST" : ""})

  def test_bag_query_for_direct_project_dependencies(self):
    """
    Check the bag can discover direct dependencies for a given requirement
    """
    requirements = self.connected_bag.requirements_for (dep.Requirement ({ "NAME" : "P1", "VERSION" : "1.0.0"}))
    
    self.assertEqual( len(requirements), 2);
    self.assertTrue( dep.Requirement(self.dep_1) in requirements, msg= str(dep.Requirement(self.dep_1) ) + "\nRESULTS: " + str(requirements) )
    self.assertTrue( dep.Requirement(self.dep_2) in requirements, msg= str(dep.Requirement(self.dep_2) ) + "\nRESULTS: " + str(requirements) )


  def test_bag_query_for_direct_project_dependencies_only_direct_dep(self):
    """
    Check the bag can discover direct dependencies for a given requirement
    """
    requirements, gr = self.connected_bag.requirements_discover (dep.Requirement ({ "NAME" : "P0", "VERSION" : "1.0.0"}))
    self.assertEqual(
      len(requirements),
      gr.number_of_nodes(),
      msg='number of dependency graph node do not match detected requirements number.'
    )
    self.assertEqual( len(requirements), 3, msg='found requirements: ' + str(requirements));
    self.assertTrue( dep.Requirement(self.dep_1) in requirements, msg= str(dep.Requirement(self.dep_1) ) + "\nRESULTS: " + str(requirements) )

  def test_bag_query_for_project_dependencies(self):
    
    requirements, gr = self.connected_bag.requirements_discover(dep.Requirement ({ "NAME" : "P1", "VERSION" : "1.0.0"}))
    self.assertEqual(
      len(requirements),
      gr.number_of_nodes(),
      msg='number of dependency graph node do not match detected requirements number.'
    )
    self.assertEqual( len(requirements), 5, msg="discovered requirements: " + str(requirements));
    self.assertTrue( dep.Requirement(self.dep_1) in requirements)
    self.assertTrue( dep.Requirement(self.dep_2) in requirements)
    
    dep_2_1 = [r for r in requirements if r.NAME == "DEP-2-1"][0]
    self.assertEqual( dep_2_1.parent, dep.Requirement(self.dep_2) )
    
  def test_bag_query_for_multiple_dependencies(self):
    """
    Check the bag can discover the dependencies graph for a list of projects.
    This is the case of building the graph of dependencies of a project
    while it is still not mantained by pony. Need this to find out the dependency graph given the
    set of dependencies listed into the json metainformations fils.
    """
    requirements, gr = self.connected_bag.requirements_discover (
      [
        dep.Requirement ( { "NAME" : "P0", "VERSION" : "1.0.0"}),
        dep.Requirement ( { "NAME" : "DEP-2"})
      ]
    )

    self.assertEqual(
      len(requirements),
      gr.number_of_nodes(),
      msg='number of dependency graph node do not match detected requirements number.\n' + str(requirements) + '\nvs\n'+ str(gr)
    )
    self.assertEqual( len(requirements), 5, msg='found requirements: ' + str(requirements));
    self.assertTrue( dep.Requirement(self.dep_1) in requirements, msg= str(dep.Requirement(self.dep_1) ) + "\nRESULTS: " + str(requirements) )


  def test_bag_query_for_project_cyrcular_dependency(self):
    """
    Checks the bag can deal, *using simple policy* with circular dependencies. Basically it do not loop infinitelly at least.
    """
    
    self.dep_circular = { "NAME" : "DEP_CIR", "VERSION" : "0.0.3", "TEST" : "",
                          "DEPENDENCIES" :  [
                                              { 
                                                "NAME" : "DEP-2",
                                                "VERSION" : "0.1.0"
                                              }
                                            ]
                        }
                        
    self.prj =          { "NAME" : "P", "VERSION" : "0.0.3", "TEST" : "",
                          "DEPENDENCIES" :  [
                                              { 
                                                "NAME" : "P1",
                                                "VERSION" : "1.0.0"
                                              },
                                              { 
                                                "NAME" : "DEP_CIR",
                                                "VERSION" : "0.0.3"
                                              }
                                            ]
                        }
                        
                        
                        
    self.connected_bag.charge(None, self.dep_circular)
    self.connected_bag.charge(None, self.prj)
    
    requirements, gr = self.connected_bag.requirements_discover( dep.Requirement ({ "NAME" : "P", "VERSION" : "0.0.3"})) 
    self.assertEqual(len(requirements), 7, msg="discovered requirements: " + str(requirements) ) 
    
    graph = self.connected_bag.requirements_graph(dep.Requirement( {"NAME" : "P", "VERSION" : "0.0.3"}))
    print ("check this")
    print(bag.to_dot_string(graph))

    
class TestCanDealWithAlternativeDependencies(unittest.TestCase):
  """
  Tests the pony project requirement detection mechanism in case of multiple alternative project dependency. 
  The pony shall be able to:
    - constrain dependency choise in order to satisfy different (but compatible in some way) request from multiple dependant projects.
    - arbitrary choose a dependency project in case multiple project instancies can fulfill requests of dependant.
    - provide feedback on the dependency graph constructed with indication of project chosed and the one considered invalid due to constraint on requirements. 
    - of course pony also provide feedback in case It is not possible to satisfy requirements due to existing constraints.
  """
  def setUp(self):
    """ Setup a reference scenario. 

    +----+              +----+                              +--------------+
    |    |------------->| PA |----------------------------->| DEP-1 v0.2.0 |
    |    |              +----+                          --->|              |
    |    |               |                             /    +--------------+
    |    |               |                            /
    | PB |               |       +--------------+    /      +--------------+
    |    |               +------>| DEP-2 v0.1.0 |---------->|              |
    |    |                       +--------------+           | DEP-1 v0.1.0 |
    |    |                                                  |              |
    |    |------------------------------------------------->|              | 
    |    |                                                  +--------------+
    +----+ 

    Notice that the dependency of PB from DEP-1 v0.1 and PA conflicts with the dependency of PA from DEP-1 v0.2.

    """

    
    self.connected_bag = Bag()
    self.connected_bag.silent = True;
    repo = self.connected_bag

    self.connected_bag.collection.delete_many({"TEST" : ""})
    self.dep_1 =    {"NAME" : "DEP-1", "VERSION" : "0.1.0", "TEST" : "" }
    self.dep_1_v2 = {"NAME" : "DEP-1", "VERSION" : "0.2.0", "TEST" : ""}
    self.dep_2 =    {"NAME" : "DEP-2", "VERSION" : "0.1.0", "TEST" : "",
                      "DEPENDENCIES" : [ 
                                        {"NAME" : "DEP-1", "VERSION" : {"$gte" : "0.0.1"}  }
                                      ] }
                                      
    self.prj =      {"NAME" : "PA", "VERSION" : "0.1.0", "TEST" : "",
                      "DEPENDENCIES" : [ 
                                        {"NAME" : "DEP-1", "VERSION" : "0.2.0"},
                                        {"NAME" : "DEP-2", "VERSION" : "0.1.0"}
                                      ] }
    
    self.pb =       {   "NAME" : "PB", "VERSION" : "0.1.0", "TEST" : "",
                      "DEPENDENCIES" : [ 
                                        {"NAME" : "PA", "VERSION" : "0.1.0"},
                                        {"NAME" : "DEP-1", "VERSION" : "0.1.0"}
                                      ] }
    
    self.connected_bag.charge(None, self.dep_1)
    self.connected_bag.charge(None, self.dep_1_v2)
    self.connected_bag.charge(None, self.dep_2)
    self.connected_bag.charge(None, self.prj)
    self.connected_bag.charge(None, self.pb)
    

  def tearDown(self):
    self.connected_bag.collection.delete_many({"TEST" : ""})
    pass


  def test_only_one_alternative_dependency(self):
    """
    Test pony can chose from alternative dependencies when it is constrained by some other requirement
    """
    
    requirements, gr = self.connected_bag.requirements_discover(dep.Requirement( {"NAME" : "PA"} ))
    self.assertEqual(len(requirements), 3, msg = """
      expected three requirement (including project itself) but found """ + str(len(requirements)) + """
      They actually are: """ + str(requirements) + """
      Requirements graph is:
      """ + to_dot_string(gr) )
    
    req_d1_v2 = dep.Requirement(self.dep_1_v2)

    self.assertTrue( req_d1_v2 in requirements, msg="""RESULTS: 
    """+ str(requirements) + """
      Requirements graph is:
      """ + to_dot_string(gr) )
  
  def test_multiple_alternative_resolved_random(self):
    """
    pony can resolve multiple alternative for dependencies using any of the available dependant package.
    """
    
    requirements, gr = self.connected_bag.requirements_discover(dep.Requirement( {"NAME" : "DEP-2"}))
    self.assertEqual(len(requirements), 2, msg = """
      expected two requirements (including project itself) but found """ + str(len(requirements)) + """
      They actually are: """ + str(requirements) )
      
    req_d1 = dep.Requirement(self.dep_1)
    req_d1_v2 = dep.Requirement(self.dep_1_v2)
    self.assertTrue( xor(req_d1 in requirements, req_d1_v2 in requirements), msg="""Actual requirements:
    """+ str(requirements) )

  def test_multiple_alternative_direct_requirements(self):
    """
    pony can detect and resolve multiple alternative direct requests using any of the available dependant package.
    The test require DEP-1 project witch is in the bag in versioni 0.1.0 and 0.2.0 so the request must be
    translated into a graph witch describe the request for both and then the graph reduced pruning alternatives.
    """
    
    requirements, gr = self.connected_bag.requirements_discover(dep.Requirement( {"NAME" : "DEP-1"}))
    self.assertEqual(len(requirements), 1, msg = """
      expected only one requirements (including project itself) but found """ + str(len(requirements)) + """
      They actually are: """ + str(requirements) )

    self.assertEqual(len(gr.nodes()), 2, msg= "expected two alternative version of DEP-1 detected into the bag.\n"+ to_dot_string(gr))
      
    req_d1 = dep.Requirement(self.dep_1)
    req_d1_v2 = dep.Requirement(self.dep_1_v2)
    self.assertTrue( xor(req_d1 in requirements, req_d1_v2 in requirements), msg="""Actual requirements:
    """+ str(requirements) )
    
  def test_conflicting_transitive_dependencies(self):
    """When pony detect conflicting transitive dependencies it must raise exception. 
    The excetion raised must carry the annotated dependency graph for log and debugging purpose. Here we check the dot representation of the dependency graph.
    It may change in future, it is up to anyone who will make changes to check the updated version of this graph is descriptive enough to show the conflicts discovered.
    """
    self.maxDiff=None
    with self.assertRaises(bag.ImpossibleConfigurationException):
        requirements, gr = self.connected_bag.requirements_discover(dep.Requirement( {"NAME" : "PB"}))
    try:
        self.connected_bag.requirements_discover(dep.Requirement( {"NAME" : "PB"}))
        self.assert_("expect it to raise exception, didn't it failed yet?\n"+ bag.to_dot_string())
    except bag.ImpossibleConfigurationException as exception_raised:
        expected_dot_graph = """digraph {
    "{ NAME:DEP-1, VERSION:0.1.0 }" [penwidth=3 ];
    "{ NAME:DEP-1, VERSION:0.2.0 }" [penwidth=3 ];
    "{ NAME:DEP-2, VERSION:0.1.0 }" [penwidth=3 ];
    "{ NAME:PA, VERSION:0.1.0 }" [penwidth=3 ];
    "{ NAME:PB, VERSION:0.1.0 }" [penwidth=3 ];

    "{ NAME:DEP-2, VERSION:0.1.0 }" -> "{ NAME:DEP-1, VERSION:0.1.0 }"[color=black penwidth=3];
    "{ NAME:DEP-2, VERSION:0.1.0 }" -> "{ NAME:DEP-1, VERSION:0.2.0 }"[color=black penwidth=3];
    "{ NAME:PA, VERSION:0.1.0 }" -> "{ NAME:DEP-1, VERSION:0.2.0 }"[color=black penwidth=3];
    "{ NAME:PA, VERSION:0.1.0 }" -> "{ NAME:DEP-2, VERSION:0.1.0 }"[color=black penwidth=3];
    "{ NAME:PB, VERSION:0.1.0 }" -> "{ NAME:DEP-1, VERSION:0.1.0 }"[color=black penwidth=3];
    "{ NAME:PB, VERSION:0.1.0 }" -> "{ NAME:PA, VERSION:0.1.0 }"[color=black penwidth=3];
}
"""
        self.assertEqual( expected_dot_graph, to_dot_string(exception_raised.gr), msg= "Unmatched graph representation, check changes please. It is expected to have conflicting dependencies requests." )
        
if __name__ == "__main__":
  unittest.main()