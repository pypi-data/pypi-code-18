import logging
import os

import cryptography.exceptions
import cryptography.hazmat.backends
import cryptography.hazmat.primitives.asymmetric
import cryptography.hazmat.primitives.hashes
import cryptography.hazmat.primitives.hmac
import cryptography.hazmat.primitives.padding
import cryptography.hazmat.primitives.serialization

LOGGER = logging.getLogger(__name__)

MASTER_KEY_PRIVATE = '/etc/maxillo/master/master.private.pem'
MASTER_KEY_PUBLIC = '/etc/maxillo/master/master.public.pem'

def has_master_key():
    return os.path.exists(MASTER_KEY_PRIVATE)

def generate_master_key():
    generate_key(MASTER_KEY_PUBLIC, MASTER_KEY_PRIVATE)

def generate_key(public_file, private_file):
    LOGGER.info("Generating new RSA key")
    key = cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key(
        backend=cryptography.hazmat.backends.default_backend(),
        public_exponent=65537,
        key_size=4096,
    )
    private_key = key.private_bytes(
        cryptography.hazmat.primitives.serialization.Encoding.PEM,
        cryptography.hazmat.primitives.serialization.PrivateFormat.PKCS8,
        cryptography.hazmat.primitives.serialization.NoEncryption(),
    )
    with open(private_file, 'wb') as f:
        f.write(private_key)
        LOGGER.info("Wrote private key to %s", private_file)

    public_key = key.public_key().public_bytes(
        cryptography.hazmat.primitives.serialization.Encoding.PEM,
        cryptography.hazmat.primitives.serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    with open(public_file, 'wb') as f:
        f.write(public_key)
        LOGGER.info("Wrote public key to %s", public_file)

def deserialize_private(key):
    return cryptography.hazmat.primitives.serialization.load_pem_private_key(
        data    = key.encode('utf-8'),
        backend = cryptography.hazmat.backends.default_backend(),
        password = None,
    )

def deserialize_public(key):
    return cryptography.hazmat.primitives.serialization.load_pem_public_key(
        data    = key.encode('utf-8'),
        backend = cryptography.hazmat.backends.default_backend(),
    )

def generate_signature(key, content):
    signer = key.signer(
        cryptography.hazmat.primitives.asymmetric.padding.PSS(
            mgf = cryptography.hazmat.primitives.asymmetric.padding.MGF1(
                cryptography.hazmat.primitives.hashes.SHA256()
            ),
            salt_length = cryptography.hazmat.primitives.asymmetric.padding.PSS.MAX_LENGTH,
        ),
        cryptography.hazmat.primitives.hashes.SHA256(),
    )
    signer.update(content)
    return signer.finalize()

def is_valid(key, signature, content):
    LOGGER.debug("Validating %s with %s and %s", key, signature, content)
    verifier = key.verifier(
        signature,
        cryptography.hazmat.primitives.asymmetric.padding.PSS(
            mgf = cryptography.hazmat.primitives.asymmetric.padding.MGF1(
                cryptography.hazmat.primitives.hashes.SHA256()
            ),
            salt_length = cryptography.hazmat.primitives.asymmetric.padding.PSS.MAX_LENGTH,
        ),
        cryptography.hazmat.primitives.hashes.SHA256(),
    )
    verifier.update(content)
    try:
        verifier.verify()
        return True
    except cryptography.exceptions.InvalidSignature:
        return False
