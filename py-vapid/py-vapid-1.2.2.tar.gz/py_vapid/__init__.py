# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import logging
import binascii
import time
import re

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives import hashes

from py_vapid.utils import b64urldecode, b64urlencode
from py_vapid.jwt import sign

# Show compliance version. For earlier versions see previously tagged releases.
VERSION = "VAPID-DRAFT-02/ECE-DRAFT-07"


class VapidException(Exception):
    """An exception wrapper for Vapid."""
    pass


class Vapid01(object):
    """Minimal VAPID Draft 01 signature generation library.

    https://tools.ietf.org/html/draft-ietf-webpush-vapid-01

    """
    _private_key = None
    _public_key = None
    _schema = "WebPush"

    def __init__(self, private_key=None):
        """Initialize VAPID with an optional private key.

        :param private_key: A private key object
        :type private_key: ecdsa.SigningKey

        """
        self.private_key = private_key
        if private_key:
            self._public_key = self.private_key.public_key()

    @classmethod
    def from_raw(cls, private_raw):
        """Initialize VAPID using a private key point in "raw" or
        "uncompressed" form. Raw keys consist of a single, 32 octet
        encoded integer.

        :param private_raw: A private key point in uncompressed form.
        :type private_raw: bytes

        """
        key = ec.derive_private_key(
            int(binascii.hexlify(b64urldecode(private_raw)), 16),
            curve=ec.SECP256R1(),
            backend=default_backend())
        return cls(key)

    @classmethod
    def from_pem(cls, private_key):
        """Initialize VAPID using a private key in PEM format.

        :param private_key: A private key in PEM format.
        :type private_key: bytes

        """
        # not sure why, but load_pem_private_key fails to deserialize
        return cls.from_der(
            b''.join(private_key.splitlines()[1:-1]))

    @classmethod
    def from_der(cls, private_key):
        """Initialize VAPID using a private key in DER format.

        :param private_key: A private key in DER format and Base64-encoded.
        :type private_key: bytes

        """
        key = serialization.load_der_private_key(b64urldecode(private_key),
                                                 password=None,
                                                 backend=default_backend())
        return cls(key)

    @classmethod
    def from_file(cls, private_key_file=None):
        """Initialize VAPID using a file containing a private key in PEM or
        DER format.

        :param private_key_file: Name of the file containing the private key
        :type private_key_file: str

        """
        if not os.path.isfile(private_key_file):
            vapid = cls()
            vapid.generate_keys()
            vapid.save_key(private_key_file)
            return vapid
        private_key = open(private_key_file, 'r').read()
        try:
            if "-----BEGIN" in private_key:
                vapid = cls.from_pem(private_key.encode('utf8'))
            else:
                vapid = cls.from_der(private_key.encode('utf8'))
            return vapid
        except Exception as exc:
            logging.error("Could not open private key file: %s", repr(exc))
            raise VapidException(exc)

    @property
    def private_key(self):
        """The VAPID private ECDSA key"""
        if not self._private_key:
            raise VapidException("No private key. Call generate_keys()")
        return self._private_key

    @private_key.setter
    def private_key(self, value):
        """Set the VAPID private ECDSA key

        :param value: the byte array containing the private ECDSA key data
        :type value: ec.EllipticCurvePrivateKey

        """
        self._private_key = value
        if value:
            self._public_key = self.private_key.public_key()

    @property
    def public_key(self):
        """The VAPID public ECDSA key

        The public key is currently read only. Set it via the `.private_key`
        method. This will autogenerate a public and private key if no value
        has been set.

        :returns ec.EllipticCurvePublicKey

        """
        return self._public_key

    def generate_keys(self):
        """Generate a valid ECDSA Key Pair."""
        self.private_key = ec.generate_private_key(ec.SECP256R1,
                                                   default_backend())

    def private_pem(self):
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

    def public_pem(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def save_key(self, key_file):
        """Save the private key to a PEM file.

        :param key_file: The file path to save the private key data
        :type key_file: str

        """
        with open(key_file, "wb") as file:
            file.write(self.private_pem())
            file.close()

    def save_public_key(self, key_file):
        """Save the public key to a PEM file.
        :param key_file: The name of the file to save the public key
        :type key_file: str

        """
        with open(key_file, "wb") as file:
            file.write(self.public_pem())
            file.close()

    def validate(self, validation_token):
        """Sign a Valdiation token from the dashboard

        :param validation_token: Short validation token from the dev dashboard
        :type validation_token: str
        :returns: corresponding token for key verification
        :rtype: str

        """
        sig = self.private_key.sign(
            validation_token,
            signature_algorithm=ec.ECDSA(hashes.SHA256()))
        verification_token = b64urlencode(sig)
        return verification_token

    def verify_token(self, validation_token, verification_token):
        """Internally used to verify the verification token is correct.

        :param validation_token: Provided validation token string
        :type validation_token: str
        :param verification_token: Generated verification token
        :type verification_token: str
        :returns: Boolean indicating if verifictation token is valid.
        :rtype: boolean

        """
        hsig = b64urldecode(verification_token.encode('utf8'))
        return self.public_key.verify(
            hsig,
            validation_token,
            signature_algorithm=ec.ECDSA(hashes.SHA256())
        )

    def _base_sign(self, claims):
        if not claims.get('exp'):
            claims['exp'] = str(int(time.time()) + 86400)
        if not re.match("mailto:.+@.+\..+",
                        claims.get('sub', ''),
                        re.IGNORECASE):
            raise VapidException(
                "Missing 'sub' from claims. "
                "'sub' is your admin email as a mailto: link.")
        if not re.match("^https?:\/\/[^\/\.:]+\.[^\/:]+(:\d+)?$",
                        claims.get("aud", ""),
                        re.IGNORECASE):
            raise VapidException(
                "Missing 'aud' from claims. "
                "'aud' is the scheme, host and optional port for this "
                "transaction e.g. https://example.com:8080")

        return claims

    def sign(self, claims, crypto_key=None):
        """Sign a set of claims.
        :param claims: JSON object containing the JWT claims to use.
        :type claims: dict
        :param crypto_key: Optional existing crypto_key header content. The
            vapid public key will be appended to this data.
        :type crypto_key: str
        :returns: a hash containing the header fields to use in
            the subscription update.
        :rtype: dict

        """
        claims = self._base_sign(claims)
        sig = sign(claims, self.private_key)
        pkey = 'p256ecdsa='
        pkey += b64urlencode(
            self.public_key.public_numbers().encode_point())
        if crypto_key:
            crypto_key = crypto_key + ';' + pkey
        else:
            crypto_key = pkey

        return {"Authorization": "{} {}".format(self._schema, sig.strip('=')),
                "Crypto-Key": crypto_key}


class Vapid02(Vapid01):
    """Minimal Vapid 02 signature generation library

    https://tools.ietf.org/html/draft-ietf-webpush-vapid-02

    """
    _schema = "vapid"

    def sign(self, claims, crypto_key=None):
        claims = self._base_sign(claims)
        sig = sign(claims, self.private_key)
        pkey = self.public_key.public_numbers().encode_point()
        return{
            "Authorization": "{schema} t={t},k={k}".format(
                schema=self._schema,
                t=sig,
                k=b64urlencode(pkey)
            )
        }


Vapid = Vapid01
