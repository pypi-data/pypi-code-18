import time
from uuid import uuid4

import boto3


class LockFailedError(Exception):
    pass


class DDBLock(object):

    def __init__(self, table_name, key, retries=3, interval_wait=0.1, region_name="us-east-1", max_live=30, owner_id=None):
        # interval_wait and max_live are both times in seconds
        self.max_live = max_live
        self.table_name = table_name
        self.client = boto3.client("dynamodb", region_name=region_name)
        self.key = key
        self.interval_wait = interval_wait
        self.retries = retries
        self.owner_id = owner_id or uuid4()

    def __enter__(self):
        tries = 0
        while 1:
            try:
                tries += 1
                self.aquire()
                return
            except Exception as e:
                if "The conditional request failed" in str(e):
                    if tries >= self.retries:
                        raise LockFailedError()
                    time.sleep(self.interval_wait)
                else:
                    raise e
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

    def release(self):
        args = {
            "TableName": self.table_name,
            "Key": {"lock_id": {"S": self.key}},
            "ConditionExpression": "#O < :owner_id)",
            "ExpressionAttributeNames": {
                "#O": "owner_id"
            },
            "ExpressionAttributeValues": {
                ":owner_id": {"N": self.owner_id}
            }
        }
        self.client.delete_item(**args)

    def aquire(self):
        ts = time.time()
        abandonment = ts - self.max_live
        args = {
            "TableName": self.table_name,
            "Item": {
                "lock_id": {"S": self.key},
                "owner_id": {"S": self.owner_id},
                "lock_ts": {"N": str(ts)},
            },
            "ConditionExpression": "attribute_not_exists(lock_id) OR (attribute_exists(lock_ts) AND #L < :abandonment)",
            "ExpressionAttributeNames": {
                "#L": "lock_ts"
            },
            "ExpressionAttributeValues": {
                ":abandonment": {"N": str(abandonment)}
            }
        }
        self.client.put_item(**args)

    def get_current(self):
        args = {
            "TableName": self.table_name,
            "Key": {"lock_id": {"S": self.key}},
            "ConsistentRead": True,
        }
        item = self.client.get_item(**args).get("Item")
        return item
