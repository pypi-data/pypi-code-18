import enum
import struct


class Network(enum.IntEnum):
    NULL = 0
    EN10MB = 1
    IEEE802 = 6
    ARCNET = 7
    SLIP = 8
    PPP = 9
    FDDI = 10
    ATM_RFC1483 = 11
    RAW_12 = 12
    PPP_SERIAL = 50
    PPP_ETHER = 51
    RAW_101 = 101
    C_HDLC = 104
    IEEE802_11 = 105
    LOOP = 108
    LINUX_SLL = 113
    LTALK = 114


class FileFormatError(Exception):
    pass


class Reader:
    GLOBAL_HDR_LEN = 24
    PKT_HDR_LEN = 16

    def __init__(self, filename):
        self._filename = filename

        with open(self._filename, 'rb') as pcap_file:
            global_hdr_bin = pcap_file.read(self.GLOBAL_HDR_LEN)
            self.pkt_hdr = struct.unpack('I H H I I I I', global_hdr_bin)
            self._magic_number = self.pkt_hdr[0]

            if self._magic_number == 0xa1b2c3d4:
                self._hdr_fmt = '< I H H I I I I'
                self._pkt_fmt = '< I I I I'
            elif self._magic_number == 0xd4c3b2a1:
                self._hdr_fmt = '> I H H I I I I'
                self._pkt_fmt = '> I I I I'
            else:
                raise FileFormatError('cannot read the PCAP file, wrong format')

            global_hdr = struct.unpack(self._hdr_fmt, global_hdr_bin)
            self.version_major = global_hdr[1]
            self.version_minor = global_hdr[2]
            self.thiszone = global_hdr[3]
            self.sigfigs = global_hdr[4]
            self.snaplen = global_hdr[5]
            self.network = global_hdr[6]

    def __repr__(self):
        return 'Reader(\'{}\')'.format(self._filename)

    def __iter__(self):
        with open(self._filename, 'rb') as pcap_file:
            pcap_file.read(self.GLOBAL_HDR_LEN)

            while True:
                data = pcap_file.read(self.PKT_HDR_LEN)

                if data == b'':
                    break

                ts_sec, ts_usec, incl_len, orig_len = struct.unpack(self._pkt_fmt, data)
                pkt_data = pcap_file.read(incl_len)
                yield ts_sec, ts_usec, incl_len, orig_len, pkt_data


class Writer:
    MAJ_VER = 2
    MIN_VER = 4
    THISZONE = 0
    SIGFIGS = 0
    SNAPLEN = 65535

    def __init__(self, filename, packets_iterable, network=Network.EN10MB, big_endian=True):
        self.packets_iterable = packets_iterable
        self.filename = filename
        self.network = network
        self._magic_number = 0xa1b2c3d4
        if big_endian:
            self._hdr_fmt = '> I H H I I I I'
            self._pkt_fmt = '> I I I I'
        else:
            self._hdr_fmt = '< I H H I I I I'
            self._pkt_fmt = '< I I I I'

    def __repr__(self):
        return 'Writer(\'{}\')'.format(self.filename)

    def write(self):
        """Writes the packets in the PCAP file"""
        with open(self.filename, 'wb') as pcap_file:
            global_hdr_bin = struct.pack(
                self._hdr_fmt,
                self._magic_number, self.MAJ_VER, self.MIN_VER, self.THISZONE, self.SIGFIGS, self.SNAPLEN, self.network
            )
            pcap_file.write(global_hdr_bin)

            for *pkt_hdr, pkt_data in self.packets_iterable:
                pkt_hdr_bin = struct.pack(self._pkt_fmt, *pkt_hdr)
                pcap_file.write(pkt_hdr_bin)
                pcap_file.write(pkt_data)



