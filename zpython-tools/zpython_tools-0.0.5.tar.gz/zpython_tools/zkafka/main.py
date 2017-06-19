import argparse
from broker_meta_management import manage_meta


def run():
    """
    This script is aime to control broker id generated strategy.

    scenarios
    ---------
    1, broker id may be conflict between each other when try to create the whole kafka cluster with quasar on aws.
    2, retirement one of the existed broker, the auto launched node with not expected broker id, e.g 1007, 1008.
    3, especially for case 2), if the new node will different broker id, we need to do manual partition assignment.

    what does this script do?
    ---------
    1, grab broker ids from remote zookeeper.
    2, calculate the first excepted id from a indicated scope, e.g [1001, 1006].
    3, create kafka log folder and meta.properties with the calculated id if it's a brand new node.
    4, or 3), update the broker id existed in the meta.properties with the new id if there is no any topic in the log
       folder, this case is aimed to solve the potential broker conflict when try to launch new cluster.
    """

    parser = argparse.ArgumentParser(description='Kafka meta.properties creation if it is not exist')
    parser.add_argument('--zookeeper-url', default="localhost:2181", help='URL of zookeeper')
    parser.add_argument('--log-dir', default="/kafka/data", help='Dir of kafka log')
    parser.add_argument('--meta-file', default="meta.properties", help='Meta file of kafka')
    parser.add_argument('--min-broker-id', type=int, default=1001, help='The min broker id, e.g 1001')
    parser.add_argument('--max-broker-id', type=int, default=1006, help='The max broker id, e.g 1006')
    args = parser.parse_args()

    manage_meta(args.zookeeper_url, args.log_dir, args.meta_file, args.min_broker_id, args.max_broker_id)
