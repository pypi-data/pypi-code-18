import os
import json

CONFIG = "eaas.conf"
ETCD = os.environ.get("EAAS_ETCD_IP", "127.0.0.1")


def find_config_file():
    """
    Starting at the current directory, work our way up to
    find a eaas.conf file.

    :return the filename, else None.
    """
    start = os.getcwd()

    while len(start) > 2:
        cfgfile = os.path.join(start, CONFIG)
        if os.path.isfile(cfgfile):
            return cfgfile
        start = os.path.dirname(start)
    return None


def load_defaults():
    """
    If we have a eaas.conf file, load it
    :return:
    """
    global ETCD
    conf = find_config_file()
    if conf:
        with open(conf, "r") as cfg:
            data = json.load(cfg)
            if "etcd" in data:
                ETCD = data["etcd"]


load_defaults()
