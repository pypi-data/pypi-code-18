import json

import requests
import yaml
from sdk.softfire.grpc import messages_pb2
from sdk.softfire.grpc.messages_pb2 import UserInfo
from sdk.softfire.main import start_manager
from sdk.softfire.manager import AbstractManager
from sdk.softfire.utils import TESTBED_MAPPING

from utils.static_config import CONFIG_FILE_PATH
from utils.utils import get_logger, get_available_resources

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
        :param payload:
        :return:
        """
        super().release_resources(user_info, payload)

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
        res_dict = yaml.load(payload)
        resource_id = res_dict.get("properties").get("resources_id")

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
        res_dict = yaml.load(payload)
        resource_id = res_dict.get("properties").get("resources_id")
        resource_data = None

        for k, v in self._resourcedata.items():
            if v.get('resource_id') == resource_id:
                resource_data = v
                testbed = k

        token = 1234  # TODO: generate and send to proxy
        tenant_id = user_info.testbed_tenants[TESTBED_MAPPING.get(testbed)]
        data = dict(experiment_id=token, tenant_id=tenant_id)

        r = requests.post(resource_data.get("url") + "SDNproxySetup", json=data,
                          headers=["Auth-Secret: " + res["secret"]])
        if r.headers.get('Content-Type') and r.headers['Content-Type'] == "application/json":
            try:
                resj = r.json()
                logger.debug("Result from SDN-Proxy: %s" % resj)
                user_flow_tables = resj.get("user-flow-tables")
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
        self.prepare_tenant(tenant_id, "fokus")

    def refresh_resources(self, user_info) -> list:
        return super().refresh_resources(user_info)


def start():
    start_manager(SdnManager(CONFIG_FILE_PATH))


if __name__ == '__main__':
    start()
