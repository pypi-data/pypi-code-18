import json

import yaml
from sdk.softfire.grpc import messages_pb2
from sdk.softfire.manager import AbstractManager

from utils.utils import get_available_physical_resources, get_logger

TESTBED_MAPPING = {
    'fokus': messages_pb2.FOKUS,
    'fokus-dev': messages_pb2.FOKUS_DEV,
    'ericsson': messages_pb2.ERICSSON,
    'ericsson-dev': messages_pb2.ERICSSON_DEV,
    'surrey': messages_pb2.SURREY,
    'surrey-dev': messages_pb2.SURREY_DEV,
    'ads': messages_pb2.ADS,
    'ads-dev': messages_pb2.ADS_DEV,
    'dt': messages_pb2.DT,
    'dt-dev': messages_pb2.DT_DEV,
    'any': messages_pb2.ANY
}

logger = get_logger(__name__)


class PDManager(AbstractManager):
    def refresh_resources(self, user_info) -> list:
        pass

    def validate_resources(self, user_info=None, payload=None) -> None:
        logger.info("Nothing to validate here")
        pass

    def release_resources(self, user_info, payload=None) -> None:
        pass

    def create_user(self, username, password):
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
                    "resource_id": resource_id,
                    "value": "please go to fraunhofer fokus in order to be able to use this resource"
                }
            ))
        return result
