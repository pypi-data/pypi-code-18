"""Python API for using blockchain.info."""
import requests

BASE_URL = 'https://blockchain.info/multiaddr?active='

def get_balance(addresses):
    req_url = BASE_URL + '|'.join(addresses)
    total_balance = 0
    response = requests.get(req_url)
    for address in response.json().get('addresses'):
        total_balance += address.get('final_balance')
    return total_balance / 100000000
