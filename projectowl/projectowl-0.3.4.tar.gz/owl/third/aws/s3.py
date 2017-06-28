"""OOP interface for S3.
"""

from cStringIO import StringIO

from owl.third.aws import common as aws_common
from owl.data import img_tools


class S3IO(object):
  """Class for managing s3 tasks.
  """
  session = None
  client = None

  def __init__(self, session=None, access_key="", secret_key="", region=""):
    """Create s3 client.
    """
    if session is not None:
      self.session = session
    else:
      self.session = aws_common.init_aws(access_key, secret_key, region)
    self.client = self.session.client("s3")

  def create_bucket(self, bucket_name):
    """Create s3 bucket.
    """
    self.client.create_bucket(Bucket=bucket_name)

  def upload_img_bin_as_file(self,
                             bucket_name,
                             img_bin,
                             img_format="png",
                             make_public=True):
    """Upload image binary data to bucket.

    Args:
      bucket_name: name of bucket.
      img_bin: image binary data.
      img_format: type of image, only support jpy or png.
      make_public: whether to make it publically accessible.
    Returns:
      url of the image on s3.
    """
    assert img_format in ["png", "jpg", "jpeg"], "img_format must be either png , jpg or jpeg."
    img_sha1 = img_tools.img_bin_to_sha1(img_bin)
    img_key_name = "{}.{}".format(img_sha1, img_format)
    upload_args = {}
    if img_format in ["jpg", "jpeg"]:
      upload_args["ContentType"] = "image/jpeg"
    if img_format == "png":
      upload_args["ContentType"] = "image/png"
    if make_public:
      upload_args["ACL"] = "public-read"
    self.client.upload_fileobj(
        StringIO(img_bin), bucket_name, img_key_name, ExtraArgs=upload_args)
    img_url = "{}/{}/{}".format(self.client.meta.endpoint_url, bucket_name,
                                img_key_name)
    return img_url

  def save_img(self, bucket_name, img_base64):
    """Save image data to bucket.

    sha1 is used as key for image data.

    Args:
      bucket_name: name of the target bucket.
      img_base64: base64 string of image.
    Returns:
      image sha1 hash as key.
    """
    img_sha1 = img_tools.base64_to_sha1(img_base64)
    self.client.put_object(Key=img_sha1, Body=img_base64, Bucket=bucket_name)
    return img_sha1

  def get_object(self, bucket_name, obj_key):
    """Get object binary data from bucket.

    Args:
      bucket_name: name of the target bucket.
      obj_key: object key.
    Returns:
      object data.
    """
    res = self.client.get_object(Bucket=bucket_name, Key=obj_key)
    obj_data = res["Body"].read()
    return obj_data
