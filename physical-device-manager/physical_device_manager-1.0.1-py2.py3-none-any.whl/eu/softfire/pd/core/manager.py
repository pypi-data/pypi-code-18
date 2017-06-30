import json

import yaml
from sdk.softfire.grpc import messages_pb2
from sdk.softfire.manager import AbstractManager
from sdk.softfire.utils import TESTBED_MAPPING

from eu.softfire.pd.utils.utils import get_available_physical_resources, get_logger

logger = get_logger(__name__)


class PhysicalResourceException(Exception):
    def __init__(self, message):
        self.message = message


class PDManager(AbstractManager):
    def refresh_resources(self, user_info) -> list:
        pass

    def validate_resources(self, user_info=None, payload=None) -> None:
        request_dict = yaml.load(payload)
        logger.info("Validating %s " % request_dict)

        resource_id = request_dict.get("properties").get('resource_id')
        if resource_id not in get_available_physical_resources().keys():
            raise PhysicalResourceException(
                "Resource id %s not in the valid options: %s" % (resource_id, VALID_RESOURCE_ID))
        pass

    def release_resources(self, user_info, payload=None) -> None:
        pass

    def create_user(self, user_info):
        pass

    def list_resources(self, user_info=None, payload=None) -> list:
        logger.info("Received List Resources")
        result = []

        for k, v in get_available_physical_resources().items():
            testbed = v.get('testbed')
            node_type = v.get('node_type')
            cardinality = int(v.get('cardinality'))
            description = v.get('description')
            resource_id = k
            result.append(messages_pb2.ResourceMetadata(resource_id=resource_id,
                                                        description=description,
                                                        cardinality=cardinality,
                                                        node_type=node_type,
                                                        testbed=TESTBED_MAPPING.get(testbed)))
        logger.info("returning %d resources" % len(result))
        return result

    def provide_resources(self, user_info, payload=None) -> list:
        result = []
        res_dict = yaml.load(payload)
        resource_id = res_dict.get("properties").get("resources_id")
        if resource_id == "fokus-cell":
            result.append(json.dumps(
                {
                    "value": "please go to fraunhofer fokus in order to be able to use this resource"
                }
            ))
        return result
