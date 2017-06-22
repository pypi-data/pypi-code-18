import getpass
import json
import re
import os
from collections import OrderedDict
from importlib.util import module_from_spec, spec_from_file_location

import requests

import base58
import libnacl
import sys


class EventReporter:

    def __init__(self):
        # init env url from args
        if len(sys.argv) == 1:
            print("\n\nUsage       : ./<script path> <agency-url>")
            print("For example : ./agent-reporter https://agency.evernym.com")
            print("\n")
            exit(1)

        self.envUrlPrefix = sys.argv[1]

        # create base dir
        agent_reporter_dir = ".agent-reporter"
        base_dir_path = os.path.join(os.path.expanduser("~"),
                                     agent_reporter_dir)
        if not os.path.exists(base_dir_path):
            os.mkdir(base_dir_path)

        # create conf file
        config_file_name = "agent-reporter-config.py"
        self.config_file_path = os.path.join(base_dir_path, config_file_name)
        if not os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'a+') as f:
                f.write('# configuration file\n')

        # init config
        self.config = self.get_installed_config(base_dir_path, config_file_name)

    def store_config(self, k, v):
        with open(self.config_file_path, 'a+') as f:
            f.write('{}="{}"\n'.format(k.lower(), v))

    def get_config(self, k):
        return self.config.__dict__.get(k.lower())


    @staticmethod
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

    # -----------------------------------------------------------------

    def start(self):

        def take_input(prompt_text, required=False, default="", onlyAlphabets=False, minLength=0, maxLength=0):
            while True:
                inp = input(prompt_text)

                if onlyAlphabets and not alias.isalpha():
                    print("    ERROR: only alphabets are expected")
                    continue

                if required and inp == "":
                    print("    ERROR: it is required field, please provide appropriate data")
                    continue

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

        try:
            print("\n\nNote: press Enter for default values\n")

            print("\nProvide report filter criteria...")
            start_date = take_input("  Enter start date (optional=Y, default=1st day of current month) [YYYY-MM-DD [hh:mm:ss]]: ", False, "")
            end_date = take_input("  Enter end date (optional=Y, default=last day of current month) [YYYY-MM-DD [hh:mm:ss]]: ", False, "")
            remote_conn_ids = take_input("  Enter enterprise ids (optional=Y, default=all): ", False, "")
            event_types = take_input("  Enter event types (optional=Y, default=all) [1=agent-created, 2=auth-req-sent, 3=con-sms-sent]: ", False, "")

            print("\nProvide report display criteria...")
            detailed = take_input("  Need detailed report (optional=Y, default=N) [Y/N]: ", False, "N")
            download = take_input("  Want to download as csv file (optional=Y, default=N) [Y/N]: ", False, "N")
            slice_by_type = take_input("  Slice by type (optional=Y, default=2) [1=years, 2=months, 3=days]: ", False, "2")
            slice_size = take_input("  Slice size, (optional=Y, default=1): ", False, "1")

            print("\nProvide signing information...")
            signing_info = ""
            while True:
                did = take_input("  DID or Locally stored alias (required=Y): ", True)
                signing_info = self.get_config(did)
                did_length = len(did)
                if not signing_info and (did_length < 22 or did_length > 23):
                    print("    ERROR: identifier length should be between 22 to 23 characters, please provide appropriate data")
                    continue
                else:
                    break

            if not signing_info:
                while True:
                    seed = getpass.getpass("  Enter signing key seed here (required=Y, hidden=True)]: ")
                    if seed == "":
                        print("    ERROR: it is required field, please provide appropriate data")
                        continue
                    elif len(seed) != 32:
                        print("    ERROR: seed needs to be exact 32 character long, please provide appropriate data")
                        continue
                    else:
                        break
            else:
                did, seed = signing_info.split(",")
                print("  signing information is fetched from config file=> did: {}".format(did))

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

            if not signing_info:
                store = take_input("\n\nDo you want to store signing information so that next time you have to only provide alias (optional=Y, default=N) [Y/N]: ", False, "N")
                if store == "Y":
                    while True:
                        alias = take_input("  Give an alias name (only alphabets): ", True, "", True)
                        signing_info = self.get_config(alias)
                        if not signing_info:
                            self.store_config(alias, did + "," + seed)
                            break
                        else:
                            print("    ERROR: alias is already used, please try again with some other name.")
                            continue
                else:
                    print("Ok, we'll not store signing information")

            ready = take_input("\nAre you ready to fire the report query (default=Y) [Target = {}] [Y/N] : ".format(self.envUrlPrefix), False, "Y")

            if ready == "Y":
                queryParam = "challenge={}&signature={}".format(challenge, sig)
                fixed_url = "{}/agent/id/{}/event".format(self.envUrlPrefix, did)
                final_url = fixed_url + "?" + queryParam
                r = requests.get(final_url)
                if download == "Y":
                    fn = r.headers['Content-Disposition']
                    fname = re.findall("filename=(.+)", fn)[0]
                    with open(fname, 'wb') as f:
                        f.write(r.content)
                    print("\nFile downloaded, check current directory for file: {}\n".format(fname))
                else:
                    print("\n=======================================================\n")
                    print(r.content.decode())
                    print("")
            else:
                print("\nOK\n")
        except Exception as e:
            print("\nError occurred: {}\n".format(repr(e)))
        except KeyboardInterrupt:
            print("\n\nExited\n")
