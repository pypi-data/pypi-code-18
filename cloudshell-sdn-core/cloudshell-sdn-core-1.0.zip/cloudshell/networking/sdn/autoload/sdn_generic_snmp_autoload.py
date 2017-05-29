import inject
import random
from cloudshell.shell.core.driver_context import AutoLoadDetails
from cloudshell.networking.autoload.networking_autoload_resource_attributes import NetworkingStandardRootAttributes
from cloudshell.networking.sdn.configuration.cloudshell_controller_configuration import CONTROLLER_HANDLER
from cloudshell.networking.autoload.networking_autoload_resource_structure import Port, Module, Chassis
from cloudshell.networking.sdn.resolution.topology_resolution import SDNTopologyResolution


class SDNGenericSNMPAutoload():
    def __init__(self, controller_handler=None, logger=None, vendor='ODL-Hellium'):

        self._controller = controller_handler
        self.topology = SDNTopologyResolution(self.controller)
        self.ports = {}

        self.relative_path = {}
        self.resource_id = {}

        self.switches_list = []
        self.leaf_switches_list = []
        self.resources = list()
        self.attributes = list()

        self.vendor = vendor

        self._logger = logger
        self._excluded_models = []

    @property
    def logger(self):
        if self._logger is None:
            try:
                self._logger = inject.instance('logger')
            except:
                raise Exception('SDNAutoload', 'Logger is none or empty')
        return self._logger

    @property
    def controller(self):
        if self._controller is None:
            # try:
            self._controller = inject.instance(CONTROLLER_HANDLER)
            # except:
            #     raise Exception('SDNAutoload', 'controller handler is none or empty')
        return self._controller

    def discover(self):
        """Load device structure and attributes: chassis, modules, submodules, ports, port-channels and power supplies

        :return: AutoLoadDetails object
        """

        self.logger.info('*' * 10)
        self.logger.info('Starting SDN SNMP Process')
        self.get_controller_details()
        # self.get_controller_properies()
        self.get_leaf_switches_list()
        self.get_switches_ports_dict()
        self.build_relative_path()
        self.add_relative_paths()
        self._get_ports_attributes()
        self._get_switches_attributes()

        result = AutoLoadDetails(resources=self.resources, attributes=self.attributes)

        self.logger.info('*' * 10)
        self.logger.info('Discover completed. The following Structure have been loaded:' +
                         '\nModel, Name, Relative Path, Uniqe Id')

        for resource in self.resources:
            self.logger.info('{0},\t\t{1},\t\t{2},\t\t{3}'.format(resource.model, resource.name,
                                                                  resource.relative_address,
                                                                  resource.unique_identifier))
        self.logger.info('------------------------------')
        for attribute in self.attributes:
            self.logger.info('{0},\t\t{1},\t\t{2}'.format(attribute.relative_address, attribute.attribute_name,
                                                          attribute.attribute_value))

        self.logger.info('*' * 10)
        self.logger.info('SNMP discovery Completed')

        return result

    def get_controller_details(self):
        """Get root element attributes

        """

        self.logger.info('Load Controller Attributes:')
        result = {'system_name': '',
                  'vendor': self.vendor,
                  'location': '',
                  'contact': 'ODL',
                  'version': ''}

        root = NetworkingStandardRootAttributes(**result)

        # setattr(root,'mac_address', AutoLoadAttribute('', 'Mac Address', mac_address))

        self.attributes.extend(root.get_autoload_resource_attributes())
        self.logger.info('Load controller Attributes completed.')

    def get_leaf_switches_list(self):
        self.leaf_switches_list = self.topology.get_leaf_switches()

    def get_switches_ports_dict(self):
        self.ports = self.topology.get_switches_ports()

    def uniqueid(self):
        seed = random.getrandbits(32)
        while True:
            yield seed
            seed += 1

    def build_relative_path(self):
        unique_sequence = self.uniqueid()
        for index, switch in enumerate(self.leaf_switches_list, start=1):
            self.resource_id[switch] = int(next(unique_sequence))
            self.relative_path[switch] = self.resource_id[switch]
        for dedicated_switch in self.ports:
            for index, port in enumerate(self.ports[dedicated_switch], start=1):
                self.resource_id[port] = int(next(unique_sequence))
                if self.resource_id.get(dedicated_switch) is not None:
                    self.relative_path[port] = self.resource_id.get(dedicated_switch)

    def add_relative_paths(self):

        port_list = self.ports
        switches_list = self.leaf_switches_list

        # for switch in switches_list:
        #    self.relative_path[switch] = str(self.relative_path[switch]) + '/' + str(self.resource_id[switch])

        for dedicated_switch in port_list:
            for port in port_list[dedicated_switch]:
                if (self.relative_path.get(port)):
                    if not type(self.relative_path[port]) == str:
                        self.relative_path[port] = str(self.relative_path[port]) + '/' + str(self.resource_id[port])

    def _get_ports_attributes(self):
        self.logger.info('Load Ports:')

        for switch, ports in self.ports.iteritems():

            for port_id, port_attrs in ports.iteritems():
                port_name = port_attrs['name']
                attribute_map = {
                    'l2_protocol_type': 1,
                     'mac': '',
                     'mtu': 2,
                     'bandwidth': int(port_attrs['bandwidth']),
                     'description': '',
                     'adjacent': '',
                     'duplex': 'Full',
                     'auto_negotiation': 'False'
                }

                port_object = Port(name=port_name, relative_path="{}/{}".format(switch, port_id),
                                   **attribute_map)
                self._add_resource(port_object)
                self.logger.info('Added ' + port_name + ' Port')

        self.logger.info('Load port completed.')

    def _get_switches_attributes(self):

        self.logger.info('Start loading Switches')
        for switch in self.leaf_switches_list:
            switch_index = self.resource_id[switch]
            # 'module_model': '',
            # 'version': '',
            # 'serial_number': switch_index
            module_details_map = {

            }

            switch_name = 'SDN Switch {0}'.format(switch_index)
            model = 'OpenVSwitch'
            # switch = 'SDN Switch'
            switch_object = Module(name=switch_name, model=model, relative_path=switch, **module_details_map)
            self._add_resource(switch_object)

        self.logger.info('Load switches completed.')

    def _add_resource(self, resource):
        """Add object data to resources and attributes lists

        :param resource: object which contains all required data for certain resource
        """

        self.resources.append(resource.get_autoload_resource_details())
        self.attributes.extend(resource.get_autoload_resource_attributes())
