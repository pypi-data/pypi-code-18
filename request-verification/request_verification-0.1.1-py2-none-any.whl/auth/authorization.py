import os
from base64 import b64encode
import hmac
import hashlib


class Md5MismatchException(Exception):
    pass


class Authorization:

    def auth(self, request):
        headers = request.headers
        try:
            client_signature = self.extract_client_signature(headers)
            valid_signature = self.build_valid_signature(headers, request.path, request.body)
            return client_signature == valid_signature
        except (KeyError, ValueError):
            return False

    def build_valid_signature(self, headers, url_path, body):
        secret_key = self.get_secret_key()
        claimed_md5 = headers["Content-Md5"]
        content_hash = hashlib.md5()
        content_hash.update(body)
        actual_md5 = b64encode(content_hash.digest())

        if not claimed_md5 == actual_md5:
            raise Md5MismatchException("Incorrect hash passed in headers!")

        string_to_sign = headers["Content-Type"] + ',' + headers["Content-Md5"] + ',' + url_path + ',' + headers["Date"]
        digest = hmac.new(secret_key, string_to_sign, hashlib.sha1).digest()
        signature = b64encode(digest)

        return signature

    def extract_client_signature(self, headers):
        client_id, signature = headers['Authorization'].split(":")
        return signature

    def get_secret_key(self):
        env = os.environ.get('APP_ENVIRONMENT')
        if env == 'DEVELOPMENT':
            secret_key = "notsosecret"
        else:
            secret_key = os.environ.get('SECRET_KEY')

        return secret_key
