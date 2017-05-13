import os

class Helper:

    @staticmethod
    def to_hex(number):
        """
        Return the given number as an Ethereum compatible hex value
        :param number: Numeric value
        :return: Ethereum compatible hex representation of number, ex: 0x4f
        """
        return format(number, '#04x')

    @staticmethod
    def generate_empty_payload(method):
        """
        Generate a new empty payload with the supplied method and empty params
        :param method: JSON-RPC payload method
        :return:
        """
        return {
            "method": method,
            "params": [],
            "jsonrpc": "2.0",
        }

    @staticmethod
    def result_or_raw(raw, result):
        if "error" in result:
            return result
        if raw:
            return result
        else:
            return result['result']


    @staticmethod
    def result_or_raw_quantity(raw, result):
        if raw:
            return result
        else:
            return int(result['result'], 16)


    @staticmethod
    def generate_tx_object(from_address, to_address, value):
        return {
            "from": from_address,
            "to": to_address,
            "value": value
        }

    @staticmethod
    def random_address():
        return "0x" + os.urandom(20)
