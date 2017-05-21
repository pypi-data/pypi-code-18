import os
import json

from findex_common.exceptions import JsonParseException
from findex_common.static_variables import DefaultPorts


class CrawlController:
    @staticmethod
    def make_valid_key(filename):
        rtn = filename.lower()

        for remove in ['-', ',', '+', '_']:
            rtn = rtn.replace(remove, ' ')

        if '.' in rtn:
            rtn = os.path.splitext(rtn)
            rtn = rtn[0].replace('.', ' ')

        if len(rtn) > 40:
            rtn = rtn[:40]
            rtn = rtn.strip()
        elif len(rtn) < 2:
            return
        return rtn

    @staticmethod
    def parse_crawl_message(data):
        if not isinstance(data, dict):
            if isinstance(data.data, bytes):
                data.data = data.data.decode("latin")
            data = json.loads(data.data)

        for c in ["resource_protocol", "server_address", "basepath"]:
            if c not in data and not data[c]:
                raise JsonParseException("Could not parse incoming message")

        if data["basepath"].endswith("/"):
            data["basepath"] = data["basepath"][:-1]
        elif not data["basepath"].startswith("/") and len(data["basepath"]) > 1:
            data["basepath"] = "/%s" % data["basepath"]

        if "display_url" not in data:
            data["display_url"] = "%s://%s%s" % (
                data["resource_protocol"], 
                data["server_address"], 
                data["basepath"])

        if "resource_port" not in data:
            data["resource_port"] = DefaultPorts().id_by_name(data["resource_protocol"])
        else:
            try:
                port = int(data["resource_port"])
                if 0 >= port >= 65536:
                    raise Exception
            except:
                raise JsonParseException("port needs to be a number between 1 and 65535")

        if "auth_user" not in data:
            data["auth_user"] = None

        if "auth_pass" not in data:
            data["auth_pass"] = None

        if "depth" in data:
            try:
                data["depth"] = int(data["depth"])
            except:
                raise JsonParseException("depth should be an integer")

        # @TODO:
        # address validation ?

        return data