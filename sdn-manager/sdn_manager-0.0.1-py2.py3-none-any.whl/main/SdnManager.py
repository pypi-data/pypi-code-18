from sdk.softfire.grpc import messages_pb2
from sdk.softfire.main import start_manager
from sdk.softfire.manager import AbstractManager

from utils.static_config import CONFIG_FILE_PATH
from utils.utils import get_logger, get_available_resources

logger = get_logger(__name__)


class SdnManager(AbstractManager):
    def release_resources(self, user_info, payload=None) -> None:
        super().release_resources(user_info, payload)

    def list_resources(self, user_info=None, payload=None) -> list:
        logger.info("Received List Resources")
        result = []

        for k, v in get_available_resources().items():
            testbed = v.get('testbed')
            node_type = v.get('node_type')
            cardinality = int(v.get('cardinality'))
            description = v.get('description')
            resource_id = k
            result.append(messages_pb2.ResourceMetadata(resource_id=resource_id,
                                                        description=description,
                                                        cardinality=cardinality,
                                                        node_type=node_type,
                                                        testbed=messages_pb2.FOKUS))
        logger.info("returning %d resources" % len(result))
        return result

    def validate_resources(self, user_info=None, payload=None) -> None:
        raise KeyError("Not Implemented")

    def provide_resources(self, user_info, payload=None) -> list:
        return super().provide_resources(user_info, payload)

    def create_user(self, username, password):
        super().create_user(username, password)

    def refresh_resources(self, user_info) -> list:
        return super().refresh_resources(user_info)

    def __init__(self, config_file=None) -> None:
        super().__init__()
        self.config_file = config_file


def start():
    start_manager(SdnManager(), CONFIG_FILE_PATH)

if __name__ == '__main__':
    start()