__version__ = '0.1.2'
from nanomsg import Socket, REQ
import os
import pandas as pd
import msgpack
import io
import datetime as dt

DEFAULT_TIMEOUT = 10000


def nano_request(socket, msg):
    socket.send(msg)
    return socket.recv()

def nano_connect(socket_name, socket_type, timeout):
    socket = Socket(socket_type)
    socket.connect(socket_name)
    socket.recv_timeout = timeout
    return socket


def nano_connect_and_request(socket_name, msg, timeout):
    socket = nano_connect(socket_name, REQ, timeout)
    ret = nano_request(socket, msg)
    socket.close()
    return ret

def msgpack_to_df(msg):
    """ the options (is_uds == False) are the same as before
    the uds have one row per leg
    there is a column called uniq that is one per instrument (ie uniq is repeated for each of the two
    uds legs
    assumes that the msg does not contain any duplicated tickers
    """

    def single_sm_to_df(spreadMarket):
        df = pd.DataFrame({
            "bid": spreadMarket["bid"],
            "ask": spreadMarket["ask"],
            "bsz": spreadMarket["bsz"],
            "asz": spreadMarket["asz"],
            "ticker": spreadMarket["ticker"],
            "leg_ticker": list(spreadMarket["leg_tickers"]),
            "leg_qty": list(spreadMarket["leg_qtys"])
        })
        return df

    def process_option_markets(cpts):
        if cpts["options"]:
            df = pd.DataFrame(list(cpts["options"])).rename(columns={"iputcall": "putcall"})
            df = df["ask bid asz bsz ticker strike putcall".split()]
            df["bid_ul"] = cpts["spot"]["bid"]
            df["ask_ul"] = cpts["spot"]["ask"]
            df["bsz_ul"] = cpts["spot"]["bsz"]
            df["asz_ul"] = cpts["spot"]["asz"]
        else:
            df = pd.DataFrame(columns="ask bid asz bsz ticker strike putcall bid_ul ask_ul bsz_ul asz_ul".split())

        df["is_uds"] = False
        return df

    cpts = msgpack.unpack(io.BytesIO(msg), use_list=True)

    if cpts["spreads"]:
        tickers = [xx["ticker"] for xx in cpts["spreads"]]
        assert len(set(tickers)) == len(tickers)
        sm = pd.concat([single_sm_to_df(_) for _ in  cpts["spreads"]])
    else:
        sm = pd.DataFrame(columns="ask bid ticker leg_ticker leg_qty".split())


    sm["is_uds"] = True
    om = process_option_markets(cpts)
    assert not om.duplicated(subset="ticker").any()

    df = pd.concat([om, sm])
    df["time"] = cpts["time"]
    df["texp"] = cpts["texp"]
    df["expiration_epoch"] = cpts["expiration_epoch"]
    df["expiration"] = pd.Timestamp(cpts["expiration_epoch"] * 1e9)
    df["product_code"] = cpts["product_code"]
    df["tick_size"] = cpts["tick_size"]
    df["curve_id"] = cpts["curve_id"]

    uniqdf = df.drop_duplicates("ticker").reset_index(drop=True)[["ticker"]]
    uniqdf["uniq"] = uniqdf.index

    df2 = uniqdf.drop_duplicates("ticker", keep="last")
    df = pd.merge(df, df2, on="ticker", how="left")
    return df


def try_get_pub_socket(socket_name):
    if(socket_name is None):
        try:
            socket_name = os.environ["PUB_SOCKET"]
        except KeyError:
            raise ValueError("could not connect to pub. please specify socket name or set PUB_SOCKET")
    return socket_name


class NanoRequester(object):
    """ for making arbitrary requests to an arbitrary socket"""
    def __init__(self, socket_name, timeout=DEFAULT_TIMEOUT):
        self.socket = nano_connect(socket_name, REQ, timeout)

    def request(self, msg):
        return nano_request(self.socket, msg)

    def close(self):
        self.socket.close()


class PubRequester(NanoRequester):
    """ assumes requests are to pub for setting socket and getting curve"""
    def __init__(self, socket_name=None, timeout=DEFAULT_TIMEOUT):
        socket_name = try_get_pub_socket(socket_name)
        super(PubRequester, self).__init__(socket_name, timeout)

    def request_curve(self, curve):
        return request_curve(self.socket, curve)


def request_curve(socket, curve):
    return msgpack_to_df(nano_request(socket, msgpack.packb(curve)))


def request_all_curves(socket):
    return list(msgpack.unpackb(nano_request(socket, msgpack.packb(-1))))


def get_pub_req_socket(socket_name=None, timeout=DEFAULT_TIMEOUT):
    socket_name = try_get_pub_socket(socket_name)
    socket = nano_connect(socket_name, REQ, timeout)
    return socket


def connect_and_request_curve(curve, **kwargs):
    socket = get_pub_req_socket(**kwargs)
    df = request_curve(socket, curve)
    socket.close()
    return df


def connect_and_request_all(**kwargs):
    socket = get_pub_req_socket(**kwargs)
    curves = request_all_curves(socket)
    socket.close()
    return curves

if __name__ == "__main__":
    df = connect_and_request_curve(117)
    print(df)
