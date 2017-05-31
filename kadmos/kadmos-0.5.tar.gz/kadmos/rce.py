import collections
import uuid
import json

from collections import OrderedDict as OrdDict
from shutil import move

class RceWorkflow(collections.OrderedDict):
    """
    The RCE workflow object is an ordered dictionary in which the RCE workflow file is stored. This class provides
    methods to enrich, adjust, and export the ordered dictionary.
    """

    # Static variables
    # TODO: Import from KadmosGraph?!
    RCE_ROLES_FUNS = ['Input Provider',  # 0
                      'XML Merger',      # 1
                      'XML Loader',      # 2
                      'XML PyMerger',    # 3
                      'CPACS Tool',      # 4
                      'Converger',       # 5
                      'Optimizer',       # 6
                      'Consistency constraint function',  # 7
                      'UXPath Filter',   # 8
                      'DOE']             # 9

    def __init__(self, *args, **kwargs):
        super(RceWorkflow, self).__init__(*args, **kwargs)

    def add_rce_node(self, rce_role, node_name, location, metadata=None):
        """
        Function to add a node to the RCE workflow.

        :param rce_role: type of RCE node (e.g. "CPACS-tool", "Input provider", "XML merger", etc.)
        :type rce_role: str
        :param node_name: name of the node
        :type node_name: str
        :param location: location of the node in the RCE GUI
        :type location: tuple
        :param metadata: any node metadata that is required (e.g. for CPACS tools)
        :type location: tuple
        :return: new entry in RCE workflow object
        :rtype: OrderedDict
        """

        # Input assertions
        assert rce_role in self.RCE_ROLES_FUNS
        assert type(node_name) is str or type(node_name) is unicode
        assert len(location) == 2
        assert type(location[0]) is int
        assert type(location[1]) is int
        assert location[0] >= 0
        assert location[1] >= 0
        assert type(metadata) is dict or metadata is None

        # Check if nodes key already exists, otherwise add it.
        if "nodes" not in self:
            self["nodes"] = []

        node_identifier = str(uuid.uuid4())
        node_location = str(location[0]) + ":" + str(location[1])
        if rce_role == self.RCE_ROLES_FUNS[0]:  # Input Provider
            new_node = OrdDict((
                ("identifier", node_identifier),
                ("name", node_name),
                ("location", node_location),
                ("active", "true"),
                ("component", OrdDict(
                    (("identifier", "de.rcenvironment.inputprovider"),
                     ("version", "3.2"),
                     ("name", "Input Provider")
                     ))
                 ),
                ("configuration", OrdDict(
                    (("storeComponentHistoryData", "true"),
                     ))
                 ),
             ))
        elif rce_role == self.RCE_ROLES_FUNS[4]:  # CPACS Tool
            assert type(metadata) is dict, 'Metadata dictionary is required for this node.'
            new_node = OrdDict((
                ("identifier", node_identifier),
                ("name", node_name),
                ("location", node_location),
                ("active", "true"),
                ("platform", metadata['platform']),
                ("component", OrdDict(
                     (("identifier", metadata['component']['identifier']),
                      ("version", metadata['component']['version']),
                      ("name", metadata['component']['name'])
                      ))
                 ),
                ("configuration", OrdDict(
                    (("chosenDeleteTempDirBehavior", "deleteWorkingDirectoriesAfterWorkflowExecution"),
                     ("executionMode", metadata['executionMode']),
                     ("storeComponentHistoryData", "true")
                     ))
                 ),
                ("staticInputs", [OrdDict(
                    (("identifier", str(uuid.uuid4())),
                     ("name", metadata['staticInputName']),
                     ("epIdentifier", None),
                     ("group", None),
                     ("datatype", "FileReference")
                     ))]
                 ),
                ("staticOutputs", [OrdDict(
                    (("identifier", str(uuid.uuid4())),
                     ("name", metadata['staticOutputName']),
                     ("epIdentifier", None),
                     ("group", None),
                     ("datatype", "FileReference")
                     ))]
                 )
            ))
        elif rce_role == self.RCE_ROLES_FUNS[8]:  # UXPath Filter
            assert type(metadata) is dict, 'Metadata dictionary is required for this node.'
            new_node = OrdDict((
                ("identifier", node_identifier),
                ("name", node_name),
                ("location", node_location),
                ("active", "true"),
                ("platform", metadata['platform']),
                ("component", OrdDict((
                    ("identifier", metadata['component']['identifier']),
                    ("version", metadata['component']['version']),
                    ("name", metadata['component']['name'])
                ))
                 ),
                ("configuration", OrdDict((
                    ("chosenDeleteTempDirBehavior", "deleteWorkingDirectoriesAfterWorkflowExecution"),
                    ("storeComponentHistoryData", "true")
                    ))
                 ),
                ("staticInputs", [OrdDict((
                    ("identifier", str(uuid.uuid4())),
                    ("name", metadata['staticInputNames'][0]),
                    ("epIdentifier", None),
                    ("group", None),
                    ("datatype", "FileReference"),
                    )), OrdDict((
                    ("identifier", str(uuid.uuid4())),
                    ("name", metadata['staticInputNames'][1]),
                    ("epIdentifier", None),
                    ("group", None),
                    ("datatype", "FileReference")
                    ))]
                 ),
                ("staticOutputs", [OrdDict((
                    ("identifier", str(uuid.uuid4())),
                    ("name", metadata['staticOutputName']),
                    ("epIdentifier", None),
                    ("group", None),
                    ("datatype", "FileReference")))]
                 )
            ))

        elif rce_role == self.RCE_ROLES_FUNS[7]:  # Consistency constraint function
            assert type(metadata) is dict, 'Metadata dictionary is required for this node.'
            new_node = OrdDict((
                ("identifier", node_identifier),
                ("name", node_name),
                ("location", node_location),
                ("active", "true"),
                ("platform", metadata['platform']),
                ("component", OrdDict(
                     (("identifier", metadata['component']['identifier']),
                      ("version", metadata['component']['version']),
                      ("name", metadata['component']['name'])
                      ))
                 ),
                ("configuration", OrdDict(
                    (("chosenDeleteTempDirBehavior", "deleteWorkingDirectoriesNever"),
                     ("storeComponentHistoryData", "true")
                     ))
                 ),
                ("staticInputs", [OrdDict(
                    (("identifier", str(uuid.uuid4())),
                     ("name", metadata['staticInputNames'][0]),
                     ("epIdentifier", None),
                     ("group", None),
                     ("datatype", "FileReference")
                     )),
                    OrdDict(
                        (("identifier", str(uuid.uuid4())),
                         ("name", metadata['staticInputNames'][1]),
                         ("epIdentifier", None),
                         ("group", None),
                         ("datatype", "FileReference")
                         ))
                ]
                 ),
                ("staticOutputs", [OrdDict(
                    (("identifier", str(uuid.uuid4())),
                     ("name", metadata['staticOutputName']),
                     ("epIdentifier", None),
                     ("group", None),
                     ("datatype", "FileReference")
                     ))]
                 )
            ))
        elif rce_role == self.RCE_ROLES_FUNS[1]:  # XML Merger
            assert type(metadata) is dict, 'Metadata dictionary is required for this node.'
            new_node = OrdDict((
                ("identifier", node_identifier),
                ("name", node_name),
                ("location", node_location),
                ("active", "true"),
                ("platform", "98737cdd4b424ab9af8f6bb636382176"),
                ("component", OrdDict(
                    (("identifier", "de.rcenvironment.xmlmerger"),
                     ("version", "3.2"),
                     ("name", "XML Merger")
                     ))),
                ("configuration", OrdDict(
                    (("mappingType", "Classic"),
                     ("storeComponentHistoryData", "true"),
                     ("xmlContent", "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<map:mappings xmlns:map=\"http://www.rcenvironment.de/2015/mapping\"\r\n              xmlns:xsl=\"http://www.w3.org/1999/XSL/Transform\">\r\n\r\n    <map:mapping>\r\n        <map:source>/"+metadata['root_name']+"</map:source>\r\n        <map:target>/"+metadata['root_name']+"</map:target>\r\n    </map:mapping>\r\n\r\n</map:mappings>")
                     ))),
                ("staticInputs", [OrdDict(
                    (("identifier", str(uuid.uuid4())),
                     ("name", "XML"),
                     ("epIdentifier", None),
                     ("group", None),
                     ("datatype", "FileReference")
                     )),
                 OrdDict(
                    (("identifier", str(uuid.uuid4())),
                     ("name", "XML to integrate"),
                     ("epIdentifier", None),
                     ("group", None),
                     ("datatype", "FileReference")
                     ))]),
                ("staticOutputs", [OrdDict(
                    (("identifier", str(uuid.uuid4())),
                     ("name", "XML"),
                     ("epIdentifier", None),
                     ("group", None),
                     ("datatype", "FileReference")
                     ))]),
            ))
        elif rce_role == self.RCE_ROLES_FUNS[2]:  # XML Loader
            assert type(metadata) is dict, 'Metadata XML string in dictionary is required for this node.'
            new_node = OrdDict((
                ("identifier", node_identifier),
                ("name", node_name),
                ("location", node_location),
                ("active", "true"),
                ("platform", "98737cdd4b424ab9af8f6bb636382176"),
                ("component", OrdDict((
                    ("identifier", "de.rcenvironment.xmlloader"),
                    ("version", "3.2"),
                    ("name", "XML Loader")
                ))),
                ("configuration", OrdDict((
                    ("storeComponentHistoryData", "true"),
                    ("xmlContent", metadata['data_schema'])
                ))),
                ("staticOutputs", [OrdDict((
                    ("identifier", str(uuid.uuid4())),
                    ("name", "XML"),
                    ("epIdentifier", None),
                    ("group", None),
                    ("datatype", "FileReference")
                ))])
            ))
        elif rce_role == self.RCE_ROLES_FUNS[3]:  # XML PyMerger
            assert type(metadata) is dict, 'Metadata dictionary is required for this node.'
            assert 'number_of_xmls' in metadata, 'Number of xmls (key: number_of_xmls) should be defined in metadata ' \
                                                 'for this node.'
            new_node = OrdDict((
                ("identifier", node_identifier),
                ("name", node_name),
                ("location", node_location),
                ("active", "true"),
                ("platform", "98737cdd4b424ab9af8f6bb636382176"),
                ("component", OrdDict((
                    ("identifier", "de.rcenvironment.integration.cpacs.CPACS-XML-merger"),
                    ("version", "0.1"),
                    ("name", "CPACS-XML-merger")
                ))),
                ("configuration", OrdDict((
                    ("chosenDeleteTempDirBehavior", "deleteWorkingDirectoriesAfterWorkflowExecution"),
                    ("n_xmls", str(metadata['number_of_xmls'])),
                    ("storeComponentHistoryData", "true")
                ))),
                ("staticInputs", [OrdDict((
                    ("identifier", str(uuid.uuid4())),
                    ("name", "xml_in_01"),
                    ("epIdentifier", None),
                    ("group", None),
                    ("datatype", "FileReference"),
                    ("metadata", OrdDict((
                        ("endpointFileName", ""),
                    ))
                     ))),
                    OrdDict((
                        ("identifier", str(uuid.uuid4())),
                        ("name", "xml_in_02"),
                        ("epIdentifier", None),
                        ("group", None),
                        ("datatype", "FileReference"),
                        ("metadata", OrdDict((
                            ("endpointFileName", ""),
                        ))
                         ))),
                    OrdDict((
                        ("identifier", str(uuid.uuid4())),
                        ("name", "xml_in_03"),
                        ("epIdentifier", None),
                        ("group", None),
                        ("datatype", "FileReference"),
                        ("metadata", OrdDict((
                            ("endpointFileName", ""),
                        ))
                         ))),
                    OrdDict((
                        ("identifier", str(uuid.uuid4())),
                        ("name", "xml_in_04"),
                        ("epIdentifier", None),
                        ("group", None),
                        ("datatype", "FileReference"),
                        ("metadata", OrdDict((
                            ("endpointFileName", ""),
                        ))
                         ))),
                    OrdDict((
                        ("identifier", str(uuid.uuid4())),
                        ("name", "xml_in_05"),
                        ("epIdentifier", None),
                        ("group", None),
                        ("datatype", "FileReference"),
                        ("metadata", OrdDict((
                            ("endpointFileName", ""),
                        ))
                         ))),
                    OrdDict((
                        ("identifier", str(uuid.uuid4())),
                        ("name", "xml_in_06"),
                        ("epIdentifier", None),
                        ("group", None),
                        ("datatype", "FileReference"),
                        ("metadata", OrdDict((
                            ("endpointFileName", ""),
                        ))
                         ))),
                    OrdDict((
                        ("identifier", str(uuid.uuid4())),
                        ("name", "xml_in_07"),
                        ("epIdentifier", None),
                        ("group", None),
                        ("datatype", "FileReference"),
                        ("metadata", OrdDict((
                            ("endpointFileName", ""),
                        ))
                         ))),
                    OrdDict((
                        ("identifier", str(uuid.uuid4())),
                        ("name", "xml_in_08"),
                        ("epIdentifier", None),
                        ("group", None),
                        ("datatype", "FileReference"),
                        ("metadata", OrdDict((
                            ("endpointFileName", ""),
                        ))
                         ))),
                    OrdDict((
                        ("identifier", str(uuid.uuid4())),
                        ("name", "xml_in_09"),
                        ("epIdentifier", None),
                        ("group", None),
                        ("datatype", "FileReference"),
                        ("metadata", OrdDict((
                            ("endpointFileName", ""),
                        ))
                         ))),
                    OrdDict((
                        ("identifier", str(uuid.uuid4())),
                        ("name", "xml_in_10"),
                        ("epIdentifier", None),
                        ("group", None),
                        ("datatype", "FileReference"),
                        ("metadata", OrdDict((
                            ("endpointFileName", ""),
                        ))
                         )))
                ]),
                ("staticOutputs", [OrdDict((
                    ("identifier", str(uuid.uuid4())),
                    ("name", "xml_file"),
                    ("epIdentifier", None),
                    ("group", None),
                    ("datatype", "FileReference")
                ))])
            ))
        elif rce_role == self.RCE_ROLES_FUNS[5]:  # Converger
            assert type(metadata) is dict, 'Metadata dictionary is required for this node.'
            new_node = OrdDict((
                    ("identifier", node_identifier),
                    ("name", node_name),
                    ("location", node_location),
                    ("active", "true"),
                    ("platform", "98737cdd4b424ab9af8f6bb636382176"),
                    ("component", OrdDict((
                        ("identifier", "de.rcenvironment.converger"),
                        ("version", "5"),
                        ("name", "Converger")
                    ))),
                     ("configuration", OrdDict((
                         ("epsA", metadata['configuration']['epsA']),
                         ("epsR", metadata['configuration']['epsR']),
                         ("isNestedLoop_5e0ed1cd", metadata['configuration']['isNestedLoop_5e0ed1cd']),
                         ("iterationsToConsider", metadata['configuration']["iterationsToConsider"]),
                         ("loopRerunAndFail_5e0ed1cd", metadata['configuration']["loopRerunAndFail_5e0ed1cd"]),
                         ("storeComponentHistoryData", metadata['configuration']["storeComponentHistoryData"])
                    ))),
                      ("staticOutputs", [OrdDict((
                          ("identifier", str(uuid.uuid4())),
                          ("name", "Converged"),
                          ("epIdentifier", None),
                          ("group", None),
                          ("datatype", "Boolean"),
                          ("metadata", OrdDict((
                              ("loopEndpointType_5e0ed1cd", "OuterLoopEndpoint"),
                        ))
                    ))), OrdDict((
                          ("identifier", str(uuid.uuid4())),
                          ("name", "Converged absolute"),
                          ("epIdentifier", None),
                          ("group", None),
                          ("datatype", "Boolean"),
                          ("metadata", OrdDict((
                              ("loopEndpointType_5e0ed1cd", "OuterLoopEndpoint"),
                        ))
                    ))), OrdDict((
                          ("identifier", str(uuid.uuid4())),
                          ("name", "Converged relative"),
                          ("epIdentifier", None),
                          ("group", None),
                          ("datatype", "Boolean"),
                          ("metadata", OrdDict((
                              ("loopEndpointType_5e0ed1cd", "OuterLoopEndpoint"),
                        ))
                    ))), OrdDict((
                          ("identifier", str(uuid.uuid4())),
                          ("name", "Done"),
                          ("epIdentifier", None),
                          ("group", None),
                          ("datatype", "Boolean"),
                          ("metadata", OrdDict((
                              ("loopEndpointType_5e0ed1cd", "OuterLoopEndpoint"),
                        ))
                    ))), OrdDict((
                          ("identifier", str(uuid.uuid4())),
                          ("name", "Outer loop done"),
                          ("epIdentifier", None),
                          ("group", None),
                          ("datatype", "Boolean"),
                          ("metadata", OrdDict((
                              ("loopEndpointType_5e0ed1cd", "InnerLoopEndpoint"),
                        ))
                    )))])))
        elif rce_role == self.RCE_ROLES_FUNS[6]:  # Optimizer
            assert type(metadata) is dict, 'Metadata dictionary is required for this node.'
            new_node = OrdDict((
                    ("identifier", node_identifier),
                    ("name", node_name),
                    ("location", node_location),
                    ("active", "true"),
                    ("platform", "98737cdd4b424ab9af8f6bb636382176"),
                    ("component", OrdDict((
                      ("identifier", "de.rcenvironment.optimizer"),
                      ("version", "7.0"),
                      ("name", "Optimizer")
                    ))),
                    ("configuration", OrdDict((
                      ("CustomDakotaPath", metadata['configuration']['CustomDakotaPath']),
                      ("algorithm", metadata['configuration']['algorithm']),
                      ("dakotaExecPath", metadata['configuration']['dakotaExecPath']),
                      ("loopFaultTolerance_5e0ed1cd", metadata['configuration']['loopFaultTolerance_5e0ed1cd']),
                      ("loopRerunAndDiscard_5e0ed1cd", metadata['configuration']['loopRerunAndDiscard_5e0ed1cd']),
                      ("loopRerunAndFail_5e0ed1cd", metadata['configuration']['loopRerunAndFail_5e0ed1cd']),
                      ("methodConfigurations", metadata['configuration']['methodConfigurations']),
                      ("optimizerPackageCode", metadata['configuration']['optimizerPackageCode']),
                      ("preCalcFilePath", metadata['configuration']['preCalcFilePath']),
                      ("storeComponentHistoryData", metadata['configuration']['storeComponentHistoryData']),
                      ("usePrecalculation", metadata['configuration']['usePrecalculation'])
                    ))),
                    ("staticOutputs", [ OrdDict((
                      ("identifier", "8be25e2b-b6f2-40fb-bbb7-b7c6971dce1a"),
                      ("name", "Done"),
                      ("epIdentifier", None),
                      ("group", None),
                      ("datatype", "Boolean"),
                      ("metadata", OrdDict((
                        ("loopEndpointType_5e0ed1cd", "OuterLoopEndpoint"),
                      )))
                    )), OrdDict((
                      ("identifier", "95a93c87-d984-442b-86ce-0a6d3220a29b"),
                      ("name", "Gradient request"),
                      ("epIdentifier", None),
                      ("group", None),
                      ("datatype", "Boolean"),
                      ("metadata", OrdDict((
                        ("loopEndpointType_5e0ed1cd", "SelfLoopEndpoint"),
                      )))
                    )), OrdDict((
                      ("identifier", "32cb964e-4c4f-435a-bb40-f99ff485f6f1"),
                      ("name", "Iteration"),
                      ("epIdentifier", None),
                      ("group", None),
                      ("datatype", "Integer"),
                      ("metadata", OrdDict((
                        ("loopEndpointType_5e0ed1cd", "SelfLoopEndpoint"),
                      )))
                    )), OrdDict((
                      ("identifier", "71c7e2d7-bd9c-4f20-af2a-c066b53a4ec9"),
                      ("name", "Outer loop done"),
                      ("epIdentifier", None),
                      ("group", None),
                      ("datatype", "Boolean"),
                      ("metadata", OrdDict((
                        ("loopEndpointType_5e0ed1cd", "InnerLoopEndpoint"),
                      )))
                    ))])
            ))
        elif rce_role == self.RCE_ROLES_FUNS[9]:  # DOE
            assert type(metadata) is dict, 'Metadata dictionary is required for this node.'
            new_node = OrdDict((
                ("identifier", node_identifier),
                ("name", node_name),
                ("location", node_location),
                ("active", "true"),
                ("platform", "98737cdd4b424ab9af8f6bb636382176"),
                ("component", OrdDict((
                    ("identifier", "de.rcenvironment.doe.v2"),
                    ("version", "3.3"),
                    ("name", "Design of Experiments")))),
                ("configuration", OrdDict((
                    ("behaviourFailedRun", metadata['configuration']['behaviourFailedRun']),
                    ("endSample", metadata['configuration']['endSample']),
                    ("isNestedLoop_5e0ed1cd", metadata['configuration']['isNestedLoop_5e0ed1cd']),
                    ("loopFaultTolerance_5e0ed1cd", metadata['configuration']['loopFaultTolerance_5e0ed1cd']),
                    ("loopRerunAndDiscard_5e0ed1cd", metadata['configuration']['loopRerunAndDiscard_5e0ed1cd']),
                    ("loopRerunAndFail_5e0ed1cd", metadata['configuration']['loopRerunAndFail_5e0ed1cd']),
                    ("method", metadata['configuration']['method']),
                    ("runNumber", metadata['configuration']['runNumber']),
                    ("seedNumber", metadata['configuration']['seedNumber']),
                    ("startSample", metadata['configuration']['startSample']),
                    ("storeComponentHistoryData", metadata['configuration']['storeComponentHistoryData']),
                    ("table", metadata['configuration']['table'])))),
                ("staticOutputs", [OrdDict((
                    ("identifier", "8b4e2040-44fb-4779-a772-ac68116e947b"),
                    ("name", "Done"),
                    ("epIdentifier", None),
                    ("group", None),
                    ("datatype", "Boolean"),
                    ("metadata", OrdDict((
                        ("loopEndpointType_5e0ed1cd", "OuterLoopEndpoint"),
                    ))))),
                    OrdDict((
                    ("identifier", "edc0b70f-1d80-42cc-b3c3-1730ce51ddc0"),
                    ("name", "Outer loop done"),
                    ("epIdentifier", None),
                    ("group", None),
                    ("datatype", "Boolean"),
                    ("metadata", OrdDict((
                        ("loopEndpointType_5e0ed1cd", "InnerLoopEndpoint"),
                    )))
                    ))])
            ))
        self["nodes"].append(new_node)

    def add_dynamic_output(self, node_idx, name, datatype, epIdentifier='default', group=None, metadata=None):
        """
        Function to add a dynamic output entry to a given node.

        :param node_idx: index of the node to which a dynamic output should be added.
        :type node_idx: int
        :param name: name of the dynamic output.
        :type name:
        :param datatype:
        :type datatype:
        :param metadata:
        :type metadata:
        :return: new entry in RCE workflow object at indicated node
        :rtype: OrderedDict
        """

        # Input assertions
        assert type(name) is str or type(name) is unicode
        assert type(datatype) is str
        assert datatype in ["FileReference", "Float"]
        assert type(metadata) is OrdDict

        # Check if node already has dynamicOutputs, otherwise add it.
        if "dynamicOutputs" not in self["nodes"][node_idx]:
            self["nodes"][node_idx]["dynamicOutputs"] = []

        new_output = OrdDict((
            ("identifier", str(uuid.uuid4())),
            ("name", name),
            ("epIdentifier", epIdentifier),
            ("group", group),
            ("datatype", datatype),
            ("metadata", metadata)))
        self["nodes"][node_idx]["dynamicOutputs"].append(new_output)

    def add_dynamic_input(self, node_idx, name, datatype, epIdentifier='default', group=None, metadata=None):
        """
        Function to add dynamic input entry to a given node.

        :param node_idx: index of the node to which a dynamic output should be added.
        :type node_idx: int
        :param name: name of the dynamic input.
        :type name:
        :param datatype:
        :type datatype:
        :param metadata:
        :type metadata:
        :return: new entry in RCE workflow object at indicated node
        :rtype: OrderedDict
        """

        # Input assertions
        assert type(name) is str or type(name) is unicode
        assert type(datatype) is str
        assert datatype in ["Float", "Boolean", "FileReference"]
        assert type(metadata) is OrdDict

        # Check if node already has dynamicInputs, otherwise add it.
        if "dynamicInputs" not in self["nodes"][node_idx]:
            self["nodes"][node_idx]["dynamicInputs"] = []

        new_input = OrdDict((
                ("identifier", str(uuid.uuid4())),
                ("name", name),
                ("epIdentifier", epIdentifier),
                ("group", group),
                ("datatype", datatype),
                ("metadata", metadata)))
        self["nodes"][node_idx]["dynamicInputs"].append(new_input)

    def adjust_static_input(self, node_idx, stat_inp_idx, new_metadata):
        """
        Function to add dynamic input entry to a given node.

        :param node_idx: index of the node to which a dynamic output should be added.
        :type node_idx: int
        :param stat_inp_idx: index of the static input list entry
        :type stat_inp_idx: int
        :param new_metadata: ordered dictionary with updated metadata
        :type new_metadata: OrderedDict
        :return: new entry in RCE workflow object at indicated node
        :rtype: OrderedDict
        """

        # Input assertions
        assert type(node_idx) is int
        assert type(stat_inp_idx) is int
        assert type(new_metadata) is OrdDict

        self["nodes"][node_idx]["staticInputs"][stat_inp_idx]["metadata"] = new_metadata

    def add_rce_connection(self, source_id, output_id, target_id, input_id):
        """
        Function to add a connection between an input and output of two nodes in the RCE workflow object.

        :param source_id: identifier of the source node
        :type source_id: str
        :param output_id: identifier of the output entry of the source node
        :type output_id: str
        :param target_id: identifier of the target node
        :type target_id: str
        :param input_id: identifier of the input entry of the target node
        :type input_id: str
        :return: new entry in the RCE workflow object
        :rtype: OrderedDict
        """

        # Input assertions
        assert type(source_id) is str
        assert type(output_id) is str
        assert type(target_id) is str
        assert type(input_id) is str

        # Check if connections key already exists, otherwise add it.
        if "connections" not in self:
            self["connections"] = []

        new_connection = OrdDict((
            ("source", source_id),
            ("output", output_id),
            ("target", target_id),
            ("input", input_id)
        ))
        self["connections"].append(new_connection)

    def add_label(self, text, location, size, colorBackground, colorText = (0,0,0), alpha = 127,
                  alignmentType = "TOPRIGHT", border = "false", textSize=9):
        """
        Function to add a label to the RCE workflow. A label is a rectangular box with text that is used as annotation.

        :param text: text to be placed in the box
        :type text: str
        :param location: location of the box in the RCE GUI (horizontal, vertical)
        :type location: tuple
        :param size: size of the box
        :type size: tuple
        :param colorBackground: background color of the box in RGB
        :type colorBackground: tuple
        :param colorText: text color of the box text in RGB
        :type colorText: tuple
        :param alpha: transparency of the annotation box
        :type alpha: int
        :param alignmentType: alignment of the text in the box (e.g. "TOPRIGHT", "CENTER", "BOTTOMLEFT", etc.)
        :type alignmentType: str
        :param border: Boolean string on whether to use a border (e.g. "true", "false")
        :type border: str
        :param textSize: size of the text in the box (e.g. 9,10,11)
        :type textSize: int
        :return: new label entry in RCE workflow object
        :rtype: OrderedDict
        """

        # Input assertions
        assert type(text) is str
        assert type(location) is tuple
        assert len(location) is 2
        assert type(size) is tuple
        assert len(size) is 2
        assert type(alpha) is int
        assert alpha >= 0
        assert alpha <= 255
        assert type(colorText) is tuple
        assert len(colorText) is 3
        assert type(colorBackground) is tuple
        assert len(colorBackground) is 3
        assert type(alignmentType) is str
        assert alignmentType in ["TOPRIGHT", "TOPCENTER", "TOPLEFT", "CENTERLEFT", "CENTER", "CENTERRIGHT",
                                 "BOTTOMLEFT", "BOTTOMCENTER", "BOTTOMRIGHT"]
        assert type(border) is str
        assert border in ["true","false"]
        assert type(textSize) is int

        # Check if labels key already exists, otherwise add it.
        if "labels" not in self:
            self["labels"] = []

        new_label = OrdDict((("identifier", str(uuid.uuid4())),
                             ("text", text),
                             ("location", str(location[0]) + ":" + str(location[1])),
                             ("size", str(size[0]) + ":" + str(size[1])),
                             ("alpha", str(alpha)),
                             ("colorText", str(colorText[0]) + ":" + str(colorText[1]) + ":" + str(colorText[2])),
                             ("colorBackground", str(colorBackground[0]) + ":" + str(colorBackground[1]) + ":"
                              + str(colorBackground[2])),
                             ("alignmentType", alignmentType),
                             ("border", border),
                             ("textSize", str(textSize))))
        self["labels"].append(new_label)

    def add_bendpoint(self, source_id, target_id, coordinates):
        """
        Function to add a bendpoint on a connection.

        :param source_id: identifier of the source node
        :type source_id: str
        :param target_id: identifier of the target node
        :type target_id: str
        :param coordinates: coordinates of the bend in the RCE GUI
        :type coordinates: tuple
        :return: new bendpoint entry in the RCE workflow object
        :rtype: OrderedDict
        """

        # Input assertions
        assert type(source_id) is str
        assert type(target_id) is str
        assert type(coordinates) is tuple
        assert len(coordinates) is 2

        # Check if bendpoints key already exists, otherwise add it.
        if "bendpoints" not in self:
            self["bendpoints"] = []

        new_bendpoint = OrdDict((("source",source_id),
                                  ("target",target_id),
                                  ("coordinates",str(coordinates[0]) + ":" + str(coordinates[1]))))
        self["bendpoints"].append(new_bendpoint)

    def export_to_wf_file(self, rce_wf_filename, rce_working_directory=None):
        """
        Function to export the RCE workflow object to a .wf-file.

        :param rce_wf_filename: name of the wf-file (e.g. 'MDA', 'MDA.wf', 'RCE_workflow')
        :type rce_wf_filename: str
        :param rce_working_directory: (optional) directory to which the workflow should be copied.
        :type rce_working_directory: str
        :return: RCE workflow file
        :rtype: file
        """

        # Input assertions
        assert type(rce_wf_filename) is str
        if rce_working_directory is not None:
            assert type(rce_working_directory) is str or type(rce_working_directory)
        if not rce_wf_filename[-3:] == '.wf':
            rce_wf_filename += '.wf'

        # Bendpoints entry in the wf-file should be double encoded.
        if "bendpoints" in self:
            encoded_bendpoints = json.dumps(self["bendpoints"])
            self["bendpoints"] = encoded_bendpoints

        # Labels entry in the wf-file should be double encoded.
        if "labels" in self:
            encoded_labels = json.dumps(self["labels"])
            self["labels"] = encoded_labels

        # Write wf-file
        with open(rce_wf_filename, 'w') as fp:
            json.dump(self, fp, indent=2)

        # Copy wf-file to requested folder
        if rce_working_directory is not None:
            assert rce_working_directory[-1] == '/', "Invalid RCE working directory ('%s') specified. " \
                                                     "Last character should be a '/'." % rce_working_directory
            move(rce_wf_filename, rce_working_directory + rce_wf_filename)

        return 'Exporting finished...'
