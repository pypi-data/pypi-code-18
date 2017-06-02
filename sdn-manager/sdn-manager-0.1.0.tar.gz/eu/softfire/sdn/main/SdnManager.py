import json
import urllib
from _md5 import md5
from datetime import datetime

import requests
import yaml
from sdk.softfire.grpc import messages_pb2
from sdk.softfire.grpc.messages_pb2 import UserInfo
from sdk.softfire.main import start_manager
from sdk.softfire.manager import AbstractManager
from sdk.softfire.utils import TESTBED_MAPPING
from urllib3.util import url

from eu.softfire.sdn.utils.static_config import CONFIG_FILE_PATH
from eu.softfire.sdn.utils.utils import get_logger, get_available_resources

logger = get_logger(__name__)


class SdnManager(AbstractManager):
    def __init__(self, config_file_path):
        super().__init__(config_file_path)
        self._resourcedata = dict()

    def prepare_tenant(self, tenant_id, testbed):
        logger.debug("checking if tenant %s is already prepared on testbed %s" % (tenant_id, testbed))
        # TODO: send tenand_id to proxy
        if testbed is messages_pb2.FOKUS:
            logger.info("calling /PrepareTenant on SDN-Proxy-FOKUS...")
            # requests.post()
            pass
        elif testbed is messages_pb2.FOKUS_DEV:
            pass
        elif testbed is messages_pb2.ERICSSON:
            pass
        elif testbed is messages_pb2.ERICSSON_DEV:
            pass

    def setup_sdn_proxy(self, token, tenant, resource_id):
        res = self._resourcedata[resource_id]
        url = res["url"]
        data = dict(experiment_id=token, tenant_id=tenant)
        r = requests.post(url, json=data, headers=["Auth-Secret: " + res["secret"]])
        if r.headers.get('Content-Type') and r.headers['Content-Type'] == "application/json":
            try:
                resj = r.json()
                logger.debug("Result from SDN-Proxy: %s" % resj)
                return resj.get("user-flow-tables")
            except ValueError as e:
                logger.error("Error reading response json: %s" % e)
                raise Exception("Can't setup SDN-Proxy")

    def release_resources(self, user_info, payload=None) -> None:
        """
        extract token from payload and delete token at the proxy
        :param user_info:
        :param payload: JSON object { "resource_id", "flow-table-range", "token", "URI", }
        :return:
        """
        try:
            pjs = json.loads(payload)
        except ValueError as e:
            logger.error("error parsing json resources: %s" % e)

        if isinstance(pjs, list):
            for pj in pjs:
                self._terminate_resource(pj)
        else:
            self._terminate_resource(pjs)

    def _terminate_resource(self, pj):
        logger.debug("Terminating resource: %s" % pj)
        if pj or len(pj):
            res_id = pj.get("resource_id")
            token = pj.get("token")
            resource_data = None
            testbed = None
            for k, v in self._resourcedata.items():
                if v.get('resource_id') == res_id:
                    resource_data = v
                    testbed = k
            if testbed is None or res_id is None:
                logger.warn("Resource not found! probaly never deployed, i will return")
                return
            targeturl = url.parse_url(resource_data.get("url")).url.join("SDNproxy", token)
            logger.info("Deleting sdn-proxy: %s" % targeturl)
            r = requests.delete(targeturl)
            logger.debug("Result: %s" % r)

    def list_resources(self, user_info=None, payload=None) -> list:
        logger.info("Received List Resources")
        logger.debug("UserInfo: %s" % user_info)
        result = []

        self._resourcedata = dict()

        for k, v in get_available_resources().items():
            testbed = v.get('testbed')
            node_type = v.get('node_type')
            cardinality = int(v.get('cardinality'))
            description = v.get('description')
            resource_id = k
            testbed_id = TESTBED_MAPPING.get(testbed)
            logger.debug("res %s Testbed ID: %s" % (resource_id, testbed_id))
            if testbed_id is not None:
                result.append(messages_pb2.ResourceMetadata(resource_id=resource_id,
                                                            description=description,
                                                            cardinality=cardinality,
                                                            node_type=node_type,
                                                            testbed=testbed_id))
                private = v.get('private')
                self._resourcedata[testbed] = dict(url=private.get('url'), secret=private.get('secret'),
                                                   resource_id=resource_id, testbed=testbed)

        logger.info("returning %d resources" % len(result))
        return result

    def validate_resources(self, user_info=None, payload=None) -> None:
        """
        Check syntax of requested resources
        :param user_info:
        :param payload:
        :return:
        """
        logger.debug("Validating resource: %s" % payload)
        res_dict = yaml.load(payload)
        logger.debug("Resource dict: %s" % res_dict)
        resource_id = res_dict.get("properties").get("resource_id")
        logger.debug("Validate resource: %s" % resource_id)
        if resource_id not in [v.get('resource_id') for k, v in self._resourcedata.items()]:
            raise KeyError("Unknown resource_id")

    def provide_resources(self, user_info, payload=None) -> list:
        """
        Call /SetupProxy API on sdn-proxy
        :param user_info:
        :param payload:
        :return:
        """
        result = list()
        logger.debug("Deploying payload %s" % payload)
        res_dict = yaml.load(yaml.load(payload))
        logger.debug("Deploying dict %s" % res_dict)
        resource_id = res_dict.get("properties").get("resource_id")

        logger.debug("Provide: res_dict: %s" % res_dict)

        resource_data = None
        testbed = None
        for k, v in self._resourcedata.items():
            if v.get('resource_id') == resource_id:
                resource_data = v
                testbed = k

        if testbed is None or resource_id is None:
            raise KeyError("Invalid resources!")

        user_name = user_info.name
        # token_string = "%s%s%s" % (resource_id, datetime.utcnow(), user_name)
        token = "%s%s%s" % (resource_id, datetime.utcnow(), user_name)
        # token = md5(token_string.encode())  # TODO: generate and send to proxy
        tenant_id = user_info.testbed_tenants[TESTBED_MAPPING.get(testbed)]
        data = dict(experiment_id=token, tenant_id=tenant_id)

        targeturl = urllib.parse.urljoin(resource_data.get("url"), "SDNproxySetup")
        logger.debug("Target SDN-Proxy URL: %s" % targeturl)
        r = requests.post(targeturl, json=data, headers={"Auth-Secret": resource_data.get("secret")})
        logger.debug("Result: %s" % r)
        if r.headers.get('Content-Type') and r.headers['Content-Type'] == "application/json":
            try:
                resj = r.json()
                logger.debug("Result from SDN-Proxy: %s" % resj)
                user_flow_tables = resj.get("user-flow-tables", None)
                api_url = resj.get("endpoint_url")
            except ValueError as e:
                logger.error("Error reading response json: %s" % e)
                raise Exception("Can't setup SDN-Proxy")

            result.append(json.dumps(
                {
                    "resource_id": resource_id,
                    "flow-table-range": user_flow_tables,
                    "token": token,
                    "URI": api_url
                }
            ))

        return result

    def create_user(self, user_info: UserInfo) -> UserInfo:
        logger.debug("create_user: UserInfo: %s" % user_info)
        tenant_id = user_info.testbed_tenants.get(messages_pb2.FOKUS)  # FIXME hardocded for FOKUS
        if tenant_id is not None:
            self.prepare_tenant(tenant_id, "fokus")
        else:
            logger.error("Tenant_id missing!")
        return user_info

    def refresh_resources(self, user_info) -> list:
        """
        used for refreshing the image list for nvf-maanger(s)
        :param user_info:
        :return:
        """
        return super().refresh_resources(user_info)


def start():
    print("""
    
                        ███████╗ ██████╗ ███████╗████████╗███████╗██╗██████╗ ███████╗                 
                        ██╔════╝██╔═══██╗██╔════╝╚══██╔══╝██╔════╝██║██╔══██╗██╔════╝                 
                        ███████╗██║   ██║█████╗     ██║   █████╗  ██║██████╔╝█████╗                   
                        ╚════██║██║   ██║██╔══╝     ██║   ██╔══╝  ██║██╔══██╗██╔══╝                   
                        ███████║╚██████╔╝██║        ██║   ██║     ██║██║  ██║███████╗                 
                        ╚══════╝ ╚═════╝ ╚═╝        ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝                 
                                                                                                      
                                                                                                      
                                                                                                      
█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗█████╗
╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝╚════╝
                                                                                                      
                                                                                                      
                                                                                                      
    ███████╗██████╗ ███╗   ██╗    ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗       
    ██╔════╝██╔══██╗████╗  ██║    ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗      
    ███████╗██║  ██║██╔██╗ ██║    ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝      
    ╚════██║██║  ██║██║╚██╗██║    ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗      
    ███████║██████╔╝██║ ╚████║    ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║      
    ╚══════╝╚═════╝ ╚═╝  ╚═══╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝      
                                                                                                      
    
    """)
    try:
        start_manager(SdnManager(CONFIG_FILE_PATH))
    except:
        logger.error("exception while shutting down...")
        exit(0)


if __name__ == '__main__':
    start()
