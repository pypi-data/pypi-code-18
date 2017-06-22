import getpass
import json
import re
import os
from collections import OrderedDict
import configparser
from importlib.util import module_from_spec, spec_from_file_location

import requests

import base58
import libnacl
import sys


def take_input(prompt_text, default=""):
    inp = input(prompt_text)
    if inp == "" and default != "":
        return default
    else:
        return inp


def sign(message, seed):

    if len(seed) != libnacl.crypto_sign_SEEDBYTES:
        raise ValueError(
            "The seed must be exactly %d bytes long" %
            libnacl.crypto_sign_SEEDBYTES
        )

    seed_str = seed.encode('utf-8')
    seed_bytes = bytes(seed_str)
    _, signing_key = libnacl.crypto_sign_seed_keypair(seed_bytes)

    ser_msg = message.encode('utf-8')
    raw_signed = libnacl.crypto_sign(ser_msg, signing_key)
    bsig = raw_signed[:libnacl.crypto_sign_BYTES]
    return base58.b58encode(bsig)


agent_reporter_dir = ".agent-reporter"
base_dir_path = os.path.join(os.path.expanduser("~"), agent_reporter_dir)

config_file_name = "agent-reporter-config.py"
config_file_path = os.path.join(base_dir_path, config_file_name)

if not os.path.exists(base_dir_path):
    os.mkdir(base_dir_path)

if not os.path.exists(config_file_path):
    with open(config_file_path, 'a+') as f:
        f.write('# configuration file\n')


def get_installed_config(install_dir_path, config_file_name):
    configPath = os.path.join(install_dir_path, config_file_name)
    if os.path.exists(configPath):
        spec = spec_from_file_location(config_file_name, configPath)
        config = module_from_spec(spec)
        spec.loader.exec_module(config)
        return config
    else:
        raise FileNotFoundError("no file found at location {}".
                                format(configPath))

config = ''
if os.path.exists(config_file_path):
    config = get_installed_config(base_dir_path, config_file_name)


def store_config(k, v):
    with open(config_file_path, 'a+') as f:
        f.write('{}="{}"\n'.format(k.lower(), v))


def get_config(k):
    return config.__dict__.get(k.lower())


# -----------------------------------------------------------------
envUrlPrefix = sys.argv[1]

print("\n\nNote: press Enter for default values\n")

print("\nProvide report filter criteria...")
start_date = take_input("  Enter start date (optional=Y, default=1st day of current month) [YYYY-MM-DD [hh:mm:ss]]: ", "")
end_date = take_input("  Enter end date (optional=Y, default=last day of current month) [YYYY-MM-DD [hh:mm:ss]]: ", "")
remote_conn_ids = take_input("  Enter enterprise ids (optional=Y, default=all): ", "")
event_types = take_input("  Enter event types (optional=Y, default=all) [1=agent-created, 2=auth-req-sent, 3=con-sms-sent]: ", "")

print("\nProvide report display criteria...")
detailed = take_input("  Need detailed report (optional=Y, default=N) [Y/N]: ", "N")
download = take_input("  Want to download as csv file (optional=Y, default=N) [Y/N]: ", "N")
slice_by_type = take_input("  Slice by type (optional=Y, default=2) [1=years, 2=months, 3=days]: ", "2")
slice_size = take_input("  Slice size, (optional=Y, default=1): ", "1")

print("\nProvide signing information...")
did = take_input("  DID or Locally stored alias (required=Y): ")
signing_info = get_config(did)

if not signing_info:
    seed = getpass.getpass("  Enter signing key seed here (required=Y): ")
    store = take_input("  Do you want to store signing information so that you have to only provide alias next time (optional=Y, default=N) [Y/N]: ", "N")
    if store == "Y":
        while True:
            alias = take_input("  Give an alias name: ")
            signing_info = get_config(alias)
            if not signing_info:
                store_config(alias, did + "," + seed)
                break
            else:
                print("    ERROR: alias is already used, please try again with some other name.")
                continue

else:
    print("signing information is fetched from config file")
    did, seed = signing_info.split(",")

requiredParams = OrderedDict([
    ("DID", did),
    ("seed", seed)
])

try:
    for k, v in requiredParams.items():
        if not v:
            print("\n'{}' is mandatory, please retry.".format(k))
            exit(1)

    challenge_dict = {
        "startDate": start_date,
        "endDate": end_date,
        "remoteConnectionIds" :remote_conn_ids,
        "types": event_types,
        "detail": detailed,
        "download": download,
        "sliceByType": slice_by_type,
        "sliceSize": slice_size
    }


    filtered_challenge_dict = dict((k, v) for k, v in challenge_dict.items() if v!="")
    challenge = json.dumps(filtered_challenge_dict)
    sig = sign(challenge, seed)

    print("\nVerify data:")
    print("  challenge: " + challenge)
    print("  signature: " + sig)

    ready = take_input("\nAre you ready (default=Y) [Target = {}] [Y/N] : ".format(envUrlPrefix), "Y")

    if ready == "Y":
        queryParam = "challenge={}&signature={}".format(challenge, sig)
        fixed_url = "{}/agent/id/{}/event".format(envUrlPrefix, did)
        final_url = fixed_url + "?" + queryParam
        r = requests.get(final_url)
        if download == "Y":
            fn = r.headers['Content-Disposition']
            fname = re.findall("filename=(.+)", fn)[0]
            with open(fname, 'wb') as f:
                f.write(r.content)
            print("\nFile downloaded, check current directory for file: {}\n".format(fname))
        else:
            print("\n")
            print(r.content.decode())
            print("\n")
    else:
        print("OK")
except Exception as e:
    print("\nError occurred: {}".format(repr(e)))
