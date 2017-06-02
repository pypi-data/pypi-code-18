"""Python API for using blockchain.info."""
import requests
from hashlib import sha256

BASE_URL = 'https://blockchain.info/multiaddr?active='
digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def decode_base58(bc, length):
    n = 0
    for char in bc:
        n = n * 58 + digits58.index(char)
    return n.to_bytes(length, 'big')
def check_bc(bc):
    bcbytes = decode_base58(bc, 25)
    return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]

def validate_address(address):
    try:
        return check_bc(address)
    except Exception:
        return False

def get_balance(addresses):
    req_url = BASE_URL + '|'.join(addresses)
    total_balance = 0
    response = requests.get(req_url)
    for address in response.json().get('addresses'):
        total_balance += address.get('final_balance')
    return total_balance / 100000000
