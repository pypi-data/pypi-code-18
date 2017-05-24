# -*- coding: utf-8 -*-

import os
import uuid
import subprocess
import shutil
import hashlib
import struct

from io import BytesIO
import gzip
import tempfile
# import Helper

if os.name == 'nt':
    CODE = 'gb2312'
elif os.name == 'posix':
    CODE = 'utf-8'

CODE1 = 'utf-8'


class SCPath(object):
    """
    @todo:个人用，路径类
    """

    def listdir(self, path):
        """
        @todo:当前路径下非隐藏目录列表，非递归
        """
        listdir = list()
        for i in os.listdir(path):
            if os.path.isdir(os.path.join(path, i)):
                if i[0] == '.':
                    pass
                else:
                    listdir.append(i)
        return listdir

    def listfile(self, path):
        """
        @todo: 当前路径下非隐藏文件列表，非递归
        """
        listfile = list()
        for i in os.listdir(path):
            if os.path.isfile(os.path.join(path, i)):
                if i[0] == '.':
                    pass
                else:
                    listfile.append(i)
        return listfile

    def listdirfile(self, path, filter_list=None):
        """
        @todo: 获取路径下非隐藏文件及目录列表，非递归
        filter_list 忽略目录
        """
        if not filter_list:
            return [i for i in os.listdir(path) if i[0] != '.']
        elif len(filter_list) == 1 and not filter_list[0]:
            return [i for i in os.listdir(path) if i[0] != '.']
        else:
            full_list = [i for i in os.listdir(path) if i[0] != '.']
            return [i for i in full_list if i not in filter_list]


def zip_data(content):
    """
    gzip压缩
    """
    zbuf = BytesIO()
    zfile = gzip.GzipFile(mode='wb', compresslevel=9, fileobj=zbuf)
    zfile.write(content)
    zfile.close()
    return zbuf.getvalue()


def zip_file(file_path, save_path):
    """
    压缩文件
    """
    open_file = open(file_path, 'rb')
    open_save = open(save_path, 'wb+')
    try:
        open_read = open_file.read()
        data = zip_data(open_read)

        head_xis = b'XIS'
        head_version = 0
        head_type1 = 1
        head_type2 = 1
        head_en_type = 0
        head_com_type = 1
        head_sour_len = len(open_read)

        # try:
        md5 = hashlib.md5()
        md5.update(open_read)
        head_md5 = md5.digest()
        # except:
        #     head_md5 = None
        randoms = str(uuid.uuid1()).split('-')[0]
        head_random = randoms.encode('utf-8')
        head_resour_len = len(data)

        head_resour_len = len(data)
        head = struct.pack('3sBBBBBI16s8sI', head_xis, head_version,
                           head_type1, head_type2,
                           head_en_type, head_com_type,
                           head_sour_len, head_md5,
                           head_random, head_resour_len)
        open_save.write(head)

    except Exception as e:
        print("压缩出错：" + str(e))
        return False, str(e)
    else:
        open_save.write(data)
        return True, ''
    finally:
        open_file.close()
        open_save.close()


def get_file_md5(file_path):
    """
    获取文件md5
    :param file_path:
    :return:
    """
    open_file = None
    str_md5 = None
    try:
        open_file = open(file_path, 'rb')
        md5 = hashlib.md5()
        str_read = ""
        while True:
            str_read = open_file.read(8096)
            if not str_read:
                break
            md5.update(str_read)
        str_md5 = md5.digest()
    finally:
        if open_file:
            open_file.close()
    return str_md5


def add_encryption(file_path, save_path, iszip):
    """
    单个文件加密
    :param file_path:
    :param save_path:
    :return: 0成功，1失败
    """
    test_path = "%s.temp" % save_path
    randoms = str(uuid.uuid1()).split('-')[0]

    file_open = open(file_path, 'rb')
    save_file = open(test_path, 'wb+')
    if iszip:
        temp = file_open.read(40)
        temp_head = struct.unpack('3sBBBBBI16s8sI', temp)
        head_sour_len = temp_head[6]
        head_md5 = temp_head[7]
        head_com_type = 1
    else:
        head_sour_len = os.path.getsize(file_path)
        head_md5 = get_file_md5(file_path)
        head_com_type = 0
    n = 0
    while True:
        byte = file_open.read(1)
        if not byte:
            break
        sbyte = struct.unpack("b", byte)
        byte_head = struct.pack('s', (randoms[n % len(randoms)]).encode('utf-8'))
        wbyte = struct.unpack("b", byte_head)
        zip_byte = struct.pack("b", sbyte[0] ^ wbyte[0])
        save_file.write(zip_byte)
        n += 1
    save_file.close()
    file_open.close()

    head_xis = b'XIS'
    head_version = 0
    head_type1 = 1
    head_type2 = 1
    head_en_type = 1
    head_random = randoms.encode('utf-8')
    head_resour_len = os.path.getsize(test_path)
    head = struct.pack('3sBBBBBI16s8sI',
                       head_xis, head_version,
                       head_type1, head_type2,
                       head_en_type, head_com_type,
                       head_sour_len, head_md5,
                       head_random, head_resour_len)

    open_file = open(test_path, 'rb')
    save_file = open(save_path, 'wb+')
    save_file.write(head)
    while True:
        byte = open_file.read()
        if not byte:
            break
        save_file.write(byte)
    open_file.close()
    save_file.close()
    if os.path.exists(test_path):
        os.remove(test_path)
    return True, ''


def clean_list(cl):
    """
    @todo: 清理列表空值
    """
    while '' in cl:
        cl.remove('')
    return cl

def combine2(src,dist,filter_file,filter_dir, infilter_dir,name):
    scpath = SCPath()
    files = scpath.listfile(src)
    for i in files:
        root_file = os.path.join(src, i)
        # shutil.copy(root_file, dist)
    combine_path = os.path.join(dist, "{0}.lua".format(name))
    open_combine = open(combine_path, 'a', encoding='utf-8')
    function_list = []
    for f in files:
        src_file_path = os.path.join(src, f)
        fn, fe = os.path.splitext(f)
        if fe in filter_file:
            print('[合并]正在处理：{0} '.format((src_file_path)))
            src_file_open = open(src_file_path, 'r', encoding='utf-8')
            try:
                src_file_read = src_file_open.read()
            finally:
                src_file_open.close()

            open_combine.write('function __{0}__()\n'.format((fn)))
            open_combine.write(src_file_read)
            open_combine.write('\nend\n\n')

            open_combine.flush()

            function_list.append(fn)
        elif fn in ['Thumbs.db'] or fn[0] == '.':
            continue
        else:
            continue
    if not os.path.getsize(combine_path):
        open_combine.close()
        os.remove(combine_path)
    else:
        open_combine.write('__PropertitesClientData__()\n')
        for i in function_list:
            if not i == 'PropertitesClientData':
                print('[合并]{0} done.'.format((i)))
                open_combine.write('__{0}__()\n'.format((i)))
        open_combine.close()
            # save_dir_split = root.split(src_path)[1]
            # if save_dir_split:
            #     if save_dir_split[0] == '/':
            #         save_dir_split = save_dir_split[1:]
            # save_dir = os.path.join(dist, i, save_dir_split)
            # save_path = os.path.join(save_dir, f)
            # if not os.path.exists(save_dir):
            #     os.makedirs(save_dir)
            # shutil.copy(src_file_path, save_path)

def combine(src, dist, filter_file, filter_dir, infilter_dir):
    """
    组合
    src  源
    dist 保存目录
    """
    print("合并脚本")
    scpath = SCPath()
    if infilter_dir != None:
        chose_dir_list = infilter_dir
    else:
        chose_dir_list = scpath.listdir(src)
    con_list = set(chose_dir_list) - set(filter_dir)

    uncon_list = set(chose_dir_list) - con_list
    root_file_list = scpath.listfile(src)

    for i in root_file_list:
        root_file = os.path.join(src, i)
        shutil.copy(root_file, dist)
    if list(uncon_list):
        for i in list(uncon_list):
            uncon_dir_path = os.path.join(src, i)
            uncon_save_dir = os.path.join(dist, i)
            shutil.copytree(uncon_dir_path, uncon_save_dir)

    for i in list(con_list):
        src_path = os.path.join(src, i)
        combine_path = os.path.join(dist, "{0}.lua".format( i))
        open_combine = open(combine_path, 'a',encoding='utf-8')
        function_list = []
        for root, dirs, files in os.walk(src_path):
            for f in files:
                src_file_path = os.path.join(root, f)
                fn, fe = os.path.splitext(f)
                if fe in filter_file:
                    print('[合并]正在处理：{0} '.format((src_file_path)))
                    src_file_open = open(src_file_path, 'r',encoding='utf-8')
                    try:
                        src_file_read = src_file_open.read()
                    finally:
                        src_file_open.close()

                    open_combine.write('function __{0}__()\n'.format((fn)))
                    open_combine.write(src_file_read)
                    open_combine.write('\nend\n\n')

                    open_combine.flush()

                    function_list.append(fn)
                elif fn in ['Thumbs.db'] or fn[0] == '.':
                    continue
                else:
                    save_dir_split = root.split(src_path)[1]
                    if save_dir_split:
                        if save_dir_split[0] == '/':
                            save_dir_split = save_dir_split[1:]
                    save_dir = os.path.join(dist, i, save_dir_split)
                    save_path = os.path.join(save_dir, f)
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                    shutil.copy(src_file_path, save_path)
        if not os.path.getsize(combine_path):
            open_combine.close()
            os.remove(combine_path)
        else:
            for i in function_list:
                print('[合并]{0} done.'.format((i)))
                open_combine.write('__{0}__()\n'.format((i)))
            open_combine.close()

    # raise Exception

    return True, ''


def complie(src, dist, filter_file, build_type):
    """
    编译
    """
    print("编译脚本")
    if build_type == "Debug":
        build_args = '-o'
    else:
        build_args = '-s -o'
    for root, dirs, files in os.walk(src):
        for f in files:
            src_file_path = os.path.join(root, f)
            save_dir_split = root.split(src)[1]
            if save_dir_split:
                if save_dir_split[0] == '/':
                    save_dir_split = save_dir_split[1:]
            save_dir = os.path.join(dist, save_dir_split)
            save_path = os.path.join(save_dir, f)
            fn, fe = os.path.splitext(f)
            if fe in filter_file:
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)

                print('[编译]luac %s %s %s ' % (build_args, save_path, src_file_path))
                cc = subprocess.check_output('luac %s %s %s ' % (build_args, save_path, src_file_path), shell=True)
                if cc:
                    print("asdfasdfasdfasf  " + cc)
                    return False, cc
            elif fn in ['Thumbs.db'] or fn[0] == '.':
                continue
            else:
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                shutil.copy(src_file_path, save_path)
    return True, ''


def compress(src, dist, filter_file):
    """
    压缩
    """
    print("压缩脚本")
    for root, dirs, files in os.walk(src):
        for f in files:
            src_file_path = os.path.join(root, f)
            save_dir_split = root.split(src)[1]
            if save_dir_split:
                if save_dir_split[0] == '/':
                    save_dir_split = save_dir_split[1:]
            save_dir = os.path.join(dist, save_dir_split)
            save_path = os.path.join(save_dir, f)
            fn, fe = os.path.splitext(f)
            if fe in filter_file:
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                print('[压缩]gzip %s ' % (f))
                zfile = zip_file(src_file_path, save_path)
                if not zfile[0]:
                    return False, zfile[1]
            elif fn in ['Thumbs.db'] or fn[0] == '.':
                continue
            else:
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                shutil.copy(src_file_path, save_path)
    return True, ''


def rename(src, filter_file, re_ext):
    """
    重命名
    """
    print("重命名脚本")
    for root, dirs, files in os.walk(src):
        for f in files:
            src_file_path = os.path.join(root, f)
            fn, fe = os.path.splitext(f)
            save_path = os.path.join(root, "%s%s" % (fn, re_ext))
            if fe in filter_file:
                os.rename(src_file_path, save_path)
            else:
                continue


def encryption(src, dist, filter_file, iszip):
    """
    加密
    """
    print("加密脚本")
    for root, dirs, files in os.walk(src):
        for f in files:
            src_file_path = os.path.join(root, f)
            save_dir_split = root.split(src)[1]
            if save_dir_split:
                if save_dir_split[0] == '/':
                    save_dir_split = save_dir_split[1:]
            save_dir = os.path.join(dist, save_dir_split)
            save_path = os.path.join(save_dir, f)
            fn, fe = os.path.splitext(f)
            if fe in filter_file:
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                print('[加密] %s ' % (fn))
                add_enc = add_encryption(src_file_path, save_path, iszip)
                if not add_enc[0]:
                    return False, add_enc[1]
            elif fn in ['Thumbs.db'] or fn[0] == '.':
                continue
            else:
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                shutil.copy(src_file_path, save_path)
    return True, ''


def process(src, output, buildType, filter_file_in, filter_dir_in, infilter_dir_in, change_ext, zip_in, encryption_in,step_callback = None):
    verifty_luac =  1 #subprocess.call('luac')
    if verifty_luac != 1:
        print("luac不存在，先下载安装lua 并添加至环境变量中")
    if not src:
        print("未选择源目录，添加 -d [arg] 参数")
    if not output:
        print("未选择保存目录，添加 -o [arg] 参数")
    if not os.path.exists(src):
        print("源目录不存在")

    if buildType != None and buildType not in ["Debug", "Release"]:
        print("编译参数不正确，仅能使用Debug及Release")
    filter_file = clean_list(filter_file_in.split(','))
    filter_dir = clean_list(filter_dir_in.split(','))
    infilter_dir = None
    if infilter_dir_in != None:
        infilter_dir = clean_list(infilter_dir_in.split(','))
    for i in filter_file:
        if i[0] != '.':
            print("过滤文件后缀 参数有误，后缀首字母必须为'.'")

    if os.path.exists(output):
        shutil.rmtree(output)

    if change_ext:
        if change_ext[0] != '.':
            change_ext = '.' + change_ext

    # 临时工作目录
    temp_dir = tempfile.mktemp()
    combine_dir = os.path.join(temp_dir, 'combine')
    build_dir = os.path.join(temp_dir, 'buildType')
    print("build_dir")
    print(build_dir)
    zip_dir = os.path.join(temp_dir, 'zip')
    print("zip_dir")
    print(zip_dir)
    encryption_dir = os.path.join(temp_dir, 'encryption')
    print("encryption_dir")
    print(encryption_dir)

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    os.mkdir(temp_dir)
    os.mkdir(combine_dir)
    os.mkdir(build_dir)
    os.mkdir(zip_dir)
    os.mkdir(encryption_dir)

    combine2(src, combine_dir, filter_file, filter_dir, infilter_dir,'clientDataConfig')

    if step_callback:
        step_callback('完成合并',0.1,fail=False)

    if buildType:
        complie(combine_dir, build_dir, filter_file, buildType)
    else:
        shutil.rmtree(build_dir)
        shutil.copytree(combine_dir, build_dir)

    if step_callback:
        step_callback('完成编译',0.25,fail=False)


    if zip_in:
        compress(build_dir, zip_dir, filter_file)
    else:
        shutil.rmtree(zip_dir)
        shutil.copytree(build_dir, zip_dir)

    if step_callback:
        step_callback('完成压缩',0.5,fail=False)

    if encryption_in:
        encryption(zip_dir, encryption_dir, filter_file, zip_in)
    else:
        shutil.rmtree(encryption_dir)
        shutil.copytree(zip_dir, encryption_dir)

    if step_callback:
        step_callback('完成加密',0.75,fail=False)

    if change_ext != ".lua":
        rename(encryption_dir, filter_file, change_ext)

    shutil.copytree(encryption_dir, output)


    if step_callback:
        step_callback('完成操作',1,fail=False)

    return

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    print("编译处理完成")

#
# if __name__ == "__main__":
#     main()
