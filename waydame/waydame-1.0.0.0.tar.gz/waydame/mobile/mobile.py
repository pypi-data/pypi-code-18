#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import codecs
import struct


class MobileSeacher(object):
    def __init__(self, path="mobile.dat"):
        if not os.path.exists(path):
            raise Exception("{0} is an invalid path".format(path))

        self.path = path
        self.data = {}

        self.__open_qqwry()
        self.__get_file_header()

        self.idx_num = (self.idx_end - self.idx_start) / 7 + 1


    def __open_qqwry(self):
        with open(self.path, "rb") as f:
            self.file_obj = mmap.mmap(
                    f.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)


    def __get_file_header(self):
        self.file_obj.seek(0)
        self.idx_start = unpack("I", self.file_obj.read(4))[0]
        self.idx_end = unpack("I", self.file_obj.read(4))[0]


    def __read_ip_from_index_block(self, offset):
        self.file_obj.seek(offset)
        tmp = self.file_obj.read(4)
        return unpack("I", tmp)[0]


    def __read_record_area_offset(self, offset):
        self.file_obj.seek(offset)
        tmp = self.file_obj.read(3)
        return unpack("I", tmp + "\0")[0]


    def __binary_search(self, target, head, tail):
        if tail - head <= 1:
            return head

        mid = (tail + head) / 2
        mid_offset = self.idx_start + mid * 7
        mid_offset_ip = self.__read_ip_from_index_block(mid_offset)
        if target > mid_offset_ip:
            return self.__binary_search(target, mid, tail)
        else:
            return self.__binary_search(target, head, mid)


    def __read_flag(self, offset):
        self.file_obj.seek(offset)
        tmp = self.file_obj.read(1)
        return ord(tmp) if tmp else 0


    def __read_value(self, offset):
        if offset == 0:
            return "N/A"

        flag = self.__read_flag(offset)
        if flag == Flag.TWO:
            tmp = self.file_obj.read(3)
            offset = unpack("I", tmp + "\0")[0]
            return self.__read_value(offset)

        buf = []
        self.file_obj.seek(offset)
        while True:
            tmp = self.file_obj.read(1)
            if tmp == "\0":
                break

            buf.append(tmp)

        return "".join(buf)


    def __read_record(self, offset):
        tmp = self.file_obj.read(1)
        flag = ord(tmp)
        if flag == Flag.ONE:
            tmp = self.file_obj.read(3)
            offset = unpack("I", tmp + "\0")[0]
            country = self.__read_value(offset)
            flag = self.__read_flag(offset)
            if flag == Flag.TWO:
                region = self.__read_value(offset + 4)
            else:
                region = self.__read_value(offset + len(country) + 1)
        elif flag == Flag.TWO:
            tmp = self.file_obj.read(3)
            cn_offset = unpack("I", tmp + "\0")[0]
            country = self.__read_value(cn_offset)
            region = self.__read_value(offset + 4)
        else:
            country = self.__read_value(offset)
            region = self.__read_value(offset + len(country) + 1)

        return (country, region)


    @lrudecorator(1000)
    def query(self, ip):
        ip = socket.inet_aton(ip)
        ip = unpack("!I", ip)[0]
        idx = self.__binary_search(ip, 0, self.idx_num - 1)
        idx_offset = self.idx_start + idx * 7
        record_offset = self.__read_record_area_offset(idx_offset + 4)
        rst = self.__read_record(record_offset + 4)

        if rst:
            country, province, city = generate(decode(rst[0]))
            return (country, province, city, decode(rst[1]))
        else:
            return None


def init(path):
    """
        初始化查询模块
    """
    pass


def search(header):
    """
        查询手机归属地
    """
    f = open("mobile.dat")
    i_length = struct.unpack("<i", f.read(4))
    print i_length


def build(path):
    """
        通过txt文件生成dat文件
        参数说明：
        path: txt文件路径

        txt文件格式：
        prefix\theader\tprov\tcity\tisp\tcode\tzip
        prefix: 手机前3位前缀
        header: 手机前7位
        prov: 所属省份
        city: 所属城市
        isp: 运营商
        code: 区号
        zip: 邮政编码
    """
    if not os.path.exists(path):
        return

    f_txt = open(path, "r")

    p_length = c_length = 0
    p_index = {}; c_index = {}
    f_content = open("content.tmp", "w")
    
    # 生成dat文件
    for l in f_txt:
        s = l.split("\t")

        prefix = s[0].strip()
        header = s[1].strip() 
        prov = s[2].strip() 
        city = s[3].strip() 
        isp = s[4].strip() 
        code = s[5].strip() 
        zip = s[6].strip() 

        if not prefix.isdigit():
            continue

        content = "%s\t%s\t%s\t%s\t%s\n" % (prov, city, isp, code, zip)

        if not c_index.has_key(content):
            c_index[content] = [ c_length, len(content) ]
            c_length += len(content)
            f_content.write(content)

        p_index[int(header)] = c_index[content]

    f_content.flush()
    f_content.close()

    start = end = content = ""
    f_index = open("index.tmp", "wb")
    for k, v in p_index.items():
        f_index.write(struct.pack("<iii", k, v[0], v[1]))

    f_index.flush()
    f_index.close()

    f_dat = open("mobile.dat", "wb")
    f_dat.write(struct.pack("<i", os.path.getsize("index.tmp")))
    f_dat.flush()
    f_dat.close()

    os.system("cat index.tmp >> mobile.dat")
    os.system("cat content.tmp >> mobile.dat")
    os.remove("index.tmp")
    os.remove("content.tmp")


if __name__ == "__main__":
    path = ""
    if len(sys.argv) > 1:
        path = sys.argv[1]

    if path:
        build(path)
