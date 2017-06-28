"""Shared services for aws.
"""

import json
import boto3


# TODO(jiefeng): to finish function.
def read_config_fn(config_fn):
  """Read configuration from file.
  """
  with open(config_fn, "r") as f:
    credential = json.load(f)
    return credential


def init_aws(access_key, secret_key, region):
  """Create aws session.
  """
  session = boto3.Session(
      aws_access_key_id=access_key,
      aws_secret_access_key=secret_key,
      region_name=region)
  return session
