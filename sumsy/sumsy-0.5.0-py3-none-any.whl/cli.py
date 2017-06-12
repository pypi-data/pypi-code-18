import argparse

from Crypto.PublicKey import RSA

from .uploader import Uploader
from .downloader import Downloader
from .keygenerator import KeyGenerator


def RSAKeyType(path):
    with open(path, 'rb') as raw_key:
        return RSA.importKey(raw_key.read())


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser.add_argument(
        '--region', default='eu-west-1', help='''AWS region (default:
        eu-west-1)''')


    upload = subparsers.add_parser('upload')
    upload.set_defaults(cls=Uploader)

    upload.add_argument(
        '--private-key', dest='rsa_key', type=RSAKeyType, required=True,
        help='''Private RSA key to use to sign the manifest''')

    upload.add_argument(
        '--bucket', required=True, help='''S3 bucket to upload files and
        manifest to''')
    upload.add_argument(
        '--prefix', required=True, help='S3 key prefix for uploaded files')
    upload.add_argument(
        '--manifest', default='latest', help='''S3 key for manifest (default:
        latest)''')

    upload.add_argument(
        'directory', metavar='SOURCE', help='''Directory to upload to S3; the
        local directory structure will be replicated in S3''')


    download = subparsers.add_parser('download')
    download.set_defaults(cls=Downloader)

    download.add_argument(
        '--public-key', dest='rsa_key', type=RSAKeyType, required=True,
        help='''Public RSA key to use to verify integrity of the manifest''')

    download.add_argument(
        '--bucket', required=True, help='''S3 bucket to download files and
        manifest from''')
    download.add_argument(
        '--manifest', default='latest', help='''S3 key for manifest (default:
        latest)''')

    download.add_argument(
        '--strip', default=0, type=int, help='''Number of path components to
        strip from downloaded files (default: 0)''')

    # TODO: caching
    download.add_argument(
        '--cache', default='.sumsy', help='''Directory to use for caching
        downloaded files (default: .sumsy)''')

    download.add_argument(
        'directory', metavar='DESTINATION', help='''Directory to download files
        to; the directory structure in S3 will be replicated locally''')


    generate_key = subparsers.add_parser('generate-key')
    generate_key.set_defaults(cls=KeyGenerator)

    generate_key.add_argument(
        '--key-size', default=4096, type=int, help='''Key length, or size (in
        bits) of the RSA modulus. Must be a multiple of 256, and no smaller than
        1024 (default: 4096)''')
    generate_key.add_argument(
        'key_name', help='''File name for the generated private key; the public
        key will use the same name with an additional '.pub' suffix''')


    config = parser.parse_args()

    if not hasattr(config, 'cls'):
        parser.print_help()
        raise SystemExit()

    return config.cls(config)


def main():
    actor = parse_args()
    actor.run()


if __name__ == '__main__':
    main()
