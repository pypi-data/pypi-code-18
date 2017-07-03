from _arbit import ffi, lib

def sha256(seed, r):
    buff = ffi.new("unsigned char[32]", seed)
    lib.sha256(buff, r)
    return bytes(buff)
