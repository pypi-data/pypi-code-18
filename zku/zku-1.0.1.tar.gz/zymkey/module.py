## @file module.py
#  @author Scott Miller
#  @version 1.0
#  @date November 17, 2016
#  @copyright Zymbit, Inc.
#  @brief Python interface class to Zymkey Application Utilities Library.
#  @details
#  This file contains a Python class which interfaces to the the Zymkey
#  Application Utilities library. This class facilitates writing user
#  space applications which use Zymkey to perform cryptographic
#  operations, such as:
#       1. Signing of payloads using ECDSA
#       2. Verification of payloads that were signed using Zymkey
#       3. Exporting the public key that matches Zymkey's private key
#       4. "Locking" and "unlocking" data objects
#       5. Generating random data
#  Additionally, there are methods for changing the i2c address (i2c units
#  only), setting tap sensitivity and controlling the LED.
from __future__ import absolute_import

import hashlib
import os

from ctypes import *

import distutils.sysconfig

from .exceptions import VerificationError, ZymkeyLibraryError
from .settings import ZYMKEY_LIBRARY_PATH
from .utils import is_string

CLOUD_ENCRYPTION_KEY = 'cloud'
ZYMKEY_ENCRYPTION_KEY = 'zymkey'

ENCRYPTION_KEYS = (
    CLOUD_ENCRYPTION_KEY,
    ZYMKEY_ENCRYPTION_KEY
)

zkalib = None
prefixes = []
for prefix in (distutils.sysconfig.get_python_lib(), ''):
    _zymkey_library_path = '{}{}'.format(prefix, ZYMKEY_LIBRARY_PATH)
    if os.path.exists(_zymkey_library_path):
        zkalib = cdll.LoadLibrary(_zymkey_library_path)
        break
    else:
        prefixes.append(os.path.dirname(_zymkey_library_path))
else:
    raise ZymkeyLibraryError('unable to find {}, checked {}'.format(os.path.basename(ZYMKEY_LIBRARY_PATH), prefixes))


## @brief The Zymkey class definition
#  @details
#  This class provides access to the Zymkey within Python
class Zymkey(object):
    ## @brief The class initialization opens and stores an instance of a
    #  Zymkey context
    def __init__(self):
        ret = self._zkOpen(byref(self._zk_ctx))
        if ret < 0:
            raise AssertionError('bad return code {!r}'.format(ret))

    ## @brief Turn the LED on
    def led_on(self):
        ret = self._zkLEDOn(self._zk_ctx)
        if ret < 0:
            raise AssertionError('bad return code {!r}'.format(ret))

    ## @brief Turn the LED off
    def led_off(self):
        ret = self._zkLEDOff(self._zk_ctx)
        if ret < 0:
            raise AssertionError('bad return code {!r}'.format(ret))

    ## @brief Flash the LED
    #  @param on_ms  The amount of time in milliseconds that the LED
    #    will be on for
    #  @param off_ms The amount of time in milliseconds that the LED
    #    will be off for. If this parameter is set to 0 (default), the
    #    off time is the same as the on time.
    #  @param num_flashes The number of on/off cycles to execute. If
    #    this parameter is set to 0 (default), the LED flashes
    #    indefinitely.
    def led_flash(self, on_ms, off_ms=0, num_flashes=0):
        if off_ms == 0:
           off_ms = on_ms
        ret = self._zkLEDFlash(self._zk_ctx, on_ms, off_ms, num_flashes)
        if ret < 0:
            raise AssertionError('bad return code {!r}'.format(ret))

    ## @brief Get some random bytes
    #  @param num_bytes The number of random bytes to get
    def get_random(self, num_bytes):
        rdata = c_void_p()
        ret = self._zkGetRandBytes(self._zk_ctx, byref(rdata), num_bytes)
        if ret < 0:
            raise AssertionError('bad return code {!r}'.format(ret))
        rc = (c_ubyte * num_bytes).from_address(rdata.value)
        rd_array = bytearray(rc)
        return rd_array

    ## @brief Deposit random data in a file
    #  @param file_path    The absolute path name for the destination file
    #  @param num_bytes The number of random bytes to get
    def create_random_file(self, file_path, num_bytes):
        ret = self._zkCreateRandDataFile(self._zk_ctx, file_path, num_bytes)
        if ret < 0:
            raise AssertionError('bad return code {!r}'.format(ret))

    ## @brief Lock up source (plaintext) data
    #  @details This method encrypts and signs a block of data.
    #  @details
    #    The zymkey has two keys that can be used for locking/unlocking
    #    operations, designated as 'shared' and 'one-way'.
    #      1. The one-way key is meant to lock up data only on the
    #         local host computer. Data encrypted using this key cannot
    #         be exported and deciphered anywhere else.
    #      2. The shared key is meant for publishing data to other
    #         sources that have the capability to generate the shared
    #         key, such as the Zymbit cloud server.
    #
    #  @param src The source (plaintext) data. If typed as a basestring,
    #    it is assumed to be an absolute file name path where the source
    #    file is located, otherwise it is assumed to contain binary
    #    data.
    #  @param dst The destination (ciphertext) data. If specified as a
    #    basestring, it is assumed to be an absolute file name path
    #    where the destination data is meant to be deposited. Otherwise,
    #    the locked data result is returned from the method call as a
    #    bytearray. The default is 'None', which means that the data
    #    will be returned to the caller as a bytearray.
    #  @param encryption_key Specifies which key will be
    #    used to lock the data up. A value of 'zymkey' (default)
    #    specifies that the Zymkey will use the one-way key. A value of
    #   'cloud' specifies that the shared key is used. Specify 'cloud' for
    #    publishing data to some other source that is able to derive the
    #    shared key (e.g. Zymbit cloud) and 'zymkey' when the data is
    #    meant to reside exclusively within the host computer.
    def lock(self, src, dst=None, encryption_key=ZYMKEY_ENCRYPTION_KEY):
        # Determine if source and destination are strings. If so, they must be
        # filenames
        src_is_file = is_string(src)
        dst_is_file = is_string(dst)
        # Prepare src if it is not specifying a filename
        if not src_is_file:
            src_sz = len(src)
            src_c_ubyte = (c_ubyte * src_sz)(*src)
        # Prepare dst if it is not specifying a filename
        if not dst_is_file:
            dst_data = c_void_p()
            dst_data_sz = c_int()

        assert encryption_key in ENCRYPTION_KEYS
        use_shared_key = encryption_key == CLOUD_ENCRYPTION_KEY

        if src_is_file and dst_is_file:
            ret = self._zkLockDataF2F(self._zk_ctx,
                                      src,
                                      dst,
                                      use_shared_key)
            if ret < 0:
                raise AssertionError('bad return code {!r}'.format(ret))

        if not src_is_file and dst_is_file:
            ret = self._zkLockDataB2F(self._zk_ctx,
                                      byref(src_c_ubyte),
                                      len(src),
                                      dst,
                                      use_shared_key)
            if ret < 0:
                raise AssertionError('bad return code {!r}'.format(ret))

        if src_is_file and not dst_is_file:
            ret = self._zkLockDataF2B(self._zk_ctx,
                                      src,
                                      byref(dst_data),
                                      byref(dst_data_sz),
                                      use_shared_key)
            if ret < 0:
                raise AssertionError('bad return code {!r}'.format(ret))
            dc = (c_ubyte * dst_data_sz.value).from_address(dst_data.value)
            data_array = bytearray(dc)
            return data_array

        if not src_is_file and not dst_is_file:
            ret = self._zkLockDataB2B(self._zk_ctx,
                                      byref(src_c_ubyte),
                                      len(src),
                                      byref(dst_data),
                                      byref(dst_data_sz),
                                      use_shared_key)
            if ret < 0:
                raise AssertionError('bad return code {!r}'.format(ret))
            dc = (c_ubyte * dst_data_sz.value).from_address(dst_data.value)
            data_array = bytearray(dc)
            return data_array

    ## @brief Unlock source (ciphertext) data.
    #  @details This method verifies a locked object signature and
    #           decrypts the associated ciphertext data.
    #
    #    The zymkey has two keys that can be used for locking/unlocking
    #    operations, designated as shared and one-way.
    #      1. The one-way key is meant to lock up data only on the
    #         local host computer. Data encrypted using this key cannot
    #         be exported and deciphered anywhere else.
    #      2. The shared key is meant for publishing data to other
    #         sources that have the capability to generate the shared
    #         key, such as the Zymbit cloud server.
    #
    #  @param src The source (ciphertext) data. If typed as a
    #    basestring, it is assumed to be an absolute file name path
    #    where the source file is located, otherwise it is assumed to
    #    contain binary data.
    #  @param dst The destination (plaintext) data. If specified as a
    #    basestring, it is assumed to be an absolute file name path
    #    where the destination data is meant to be deposited. Otherwise,
    #    the locked data result is returned from the method call as a
    #    bytearray. The default is 'None', which means that the data
    #    will be returned to the caller as a bytearray.
    #  @param encryption_key Specifies which key will be
    #    used to unlock the source data. A value of 'zymkey' (default)
    #    specifies that the Zymkey will use the one-way key. A value of
    #    'cloud' specifies that the shared key is used. Specify 'cloud'
    #    for publishing data to another source that has the shared key
    #    (e.g. Zymbit cloud) and 'zymkey' when the data is meant to
    #    reside exclusively withing the host computer.
    def unlock(self, src, dst=None, encryption_key=ZYMKEY_ENCRYPTION_KEY):
        # Determine if source and destination are strings. If so, they must be
        # filenames
        src_is_file = is_string(src)
        dst_is_file = is_string(dst)

        assert encryption_key in ENCRYPTION_KEYS
        use_shared_key = encryption_key == CLOUD_ENCRYPTION_KEY

        # Prepare src if it is not specifying a filename
        if not src_is_file:
            src_sz = len(src)
            src_c_ubyte = (c_ubyte * src_sz)(*src)
        # Prepare dst if it is not specifying a filename
        if not dst_is_file:
            dst_data = c_void_p()
            dst_data_sz = c_int()

        if src_is_file and dst_is_file:
            ret = self._zkUnlockDataF2F(self._zk_ctx,
                                        src,
                                        dst,
                                        use_shared_key)
            if ret < 0:
                raise AssertionError('bad return code {!r}'.format(ret))

        if not src_is_file and dst_is_file:
            ret = self._zkUnlockDataB2F(self._zk_ctx,
                                        byref(src_c_ubyte),
                                        len(src),
                                        dst,
                                        use_shared_key)
            if ret < 0:
                raise AssertionError('bad return code {!r}'.format(ret))

        if src_is_file and not dst_is_file:
            ret = self._zkUnlockDataF2B(self._zk_ctx,
                                        src,
                                        byref(dst_data),
                                        byref(dst_data_sz),
                                        use_shared_key)
            if ret < 0:
                raise AssertionError('bad return code {!r}'.format(ret))
            dc = (c_ubyte * dst_data_sz.value).from_address(dst_data.value)
            data_array = bytearray(dc)
            return data_array

        if not src_is_file and not dst_is_file:
            ret = self._zkUnlockDataB2B(self._zk_ctx,
                                        byref(src_c_ubyte),
                                        len(src),
                                        byref(dst_data),
                                        byref(dst_data_sz),
                                        use_shared_key)
            if ret < 0:
                raise AssertionError('bad return code {!r}'.format(ret))
            dc = (c_ubyte * dst_data_sz.value).from_address(dst_data.value)
            data_array = bytearray(dc)
            return data_array

    ## @brief Generate a signature using the Zymkey's ECDSA private key.
    #  @param src This parameter contains the digest of the data that
    #    will be used to generate the signature.
    #  @returns a byte array of the signature
    #  @todo Allow for overloading of source parameter in similar
    #    fashion to lock/unlockData.
    def sign(self, src):
        sha256 = hashlib.sha256()
        sha256.update(src)

        return self.sign_digest(sha256)

    ## @brief Generate a signature using the Zymkey's ECDSA private key.
    #  @param sha256 A hashlib.sha256 instance.
    #  @todo Allow for overloading of source parameter in similar
    #    fashion to lock/unlockData.
    def sign_digest(self, sha256):
        digest_bytes = bytearray(sha256.digest())

        src_sz = len(digest_bytes)
        src_c_ubyte = (c_ubyte * src_sz)(*digest_bytes)
        dst_data = c_void_p()
        dst_data_sz = c_int()

        # was a kwarg with default value of 0 hardcoded for now
        # TODO: re-add as kwarg and remove this when implementation is complete
        sigtype = 0

        ret = self._zkGenECDSASigFromDigest(
            self._zk_ctx,
            src_c_ubyte,
            sigtype,
            byref(dst_data),
            byref(dst_data_sz)
        )
        if ret < 0:
            raise AssertionError('bad return code {!r}'.format(ret))
        dc = (c_ubyte * dst_data_sz.value).from_address(dst_data.value)
        data_array = bytearray(dc)
        return data_array

    ## @brief Verify the given buffer against the given signature.
    #    The public key is not specified in the parameter list to ensure
    #    that the public key that matches the Zymkey's ECDSA private key
    #    is used.
    #  @param src The buffer to verify
    #  @param sig This parameter contains the signature to verify.
    #  @param raise_exception By default, when verification fails a
    #    VerificationError will be raised, unless this is set to False
    #  @returns True for a good verification or False for a bad verification when raise_exception is False
    #  @todo Allow for overloading of source parameter in similar
    #    fashion to lock/unlockData.
    def verify(self, src, sig, raise_exception=True):
        sha256 = hashlib.sha256()
        sha256.update(src)

        return self.verify_digest(sha256, sig, raise_exception=raise_exception)

    ## @brief Verify a signature using the Zymkey's ECDSA public key.
    #    The public key is not specified in the parameter list to ensure
    #    that the public key that matches the Zymkey's ECDSA private key
    #    is used.
    #  @param sha256 A hashlib.sha256 instance that
    #    will be used to generate the signature.
    #  @param sig This parameter contains the signature to verify.
    #  @param raise_exception By default, when verification fails a
    #    VerificationError will be raised, unless this is set to False
    #  @returns True for a good verification or False for a bad verification when raise_exception is False
    #  @todo Allow for overloading of source parameter in similar
    #    fashion to lock/unlockData.
    def verify_digest(self, sha256, sig, raise_exception=True):
        digest_bytes = bytearray(sha256.digest())

        src_sz = len(digest_bytes)
        sig_sz = len(sig)
        src_c_ubyte = (c_ubyte * src_sz)(*digest_bytes)
        sig_c_ubyte = (c_ubyte * sig_sz)(*sig)

        # was a kwarg with default value of 0 hardcoded for now
        # TODO: re-add as kwarg and remove this when implementation is complete
        sigtype = 0

        ret = self._zkVerifyECDSASigFromDigest(
            self._zk_ctx,
            src_c_ubyte,
            sigtype,
            sig_c_ubyte,
            sig_sz
        )

        if ret == 0:
            if raise_exception:
                raise VerificationError()

            return False
        if ret == 1:
            return True
        else:
            raise AssertionError('bad return code {!r}'.format(ret))

    ## @brief Create a file with the PEM-formatted ECEDSA public key.
    #  @details This method is useful for generating a Certificate
    #           Signing Request.
    #  @param filename The absolute file path where the public key will
    #    be stored in PEM format.
    def create_ecdsa_public_key_file(self, filename):
        # was a kwarg with default value of 0 hardcoded for now
        # TODO: re-add as kwarg and remove this when implementation is complete
        slot = 0

        ret = self._zkSaveECDSAPubKey2File(self._zk_ctx, filename, slot)
        if ret < 0:
            raise AssertionError('bad return code {!r}'.format(ret))

    ## @brief Retrieves the ECEDSA public key as a binary bytearray.
    def get_ecdsa_public_key(self):
        dst_data = c_void_p()
        dst_data_sz = c_int()

        # was a kwarg with default value of 0 hardcoded for now
        # TODO: re-add as kwarg and remove this when implementation is complete
        slot = 0

        ret = self._zkGetECDSAPubKey(self._zk_ctx, byref(dst_data), byref(dst_data_sz), slot)
        if ret < 0:
            raise AssertionError('bad return code {!r}'.format(ret))
        dc = (c_ubyte * dst_data_sz.value).from_address(dst_data.value)
        data_array = bytearray(dc)
        return data_array

    ## @brief Sets the i2c address of the Zymkey (i2c versions only)
    #  @details This method should be called if the i2c address of the
    #    Zymkey is shared with another i2c device on the same i2c bus.
    #    The default i2c address for Zymkey units is 0x30. Currently,
    #    the address may be set in the ranges of 0x30 - 0x37 and
    #    0x60 - 0x67.
    #
    #    After successful completion of this command, the Zymkey will
    #    reset itself.
    #  @param address The i2c address that the Zymkey will set itself
    #    to.
    def set_i2c_address(self, address):
        addr_c_int = c_int()
        ret = self._zkSetI2CAddr(self._zk_ctx, addr_c_int)
        if ret < 0:
            raise AssertionError('bad return code {!r}'.format(ret))

    ## @brief Sets the sensitivity of tap operations.
    #  @details This method permits setting the sensitivity of the tap
    #           detection feature. Each axis may be individually
    #           configured or all at once.
    # @param axis The axis to configure. Valid values include:
    #   1. 'all': Configure all axes with the specified sensitivity
    #      value.
    #   2. 'x' or 'X': Configure only the x-axis
    #   3. 'y' or 'Y': Configure only the y-axis
    #   4. 'z' or 'Z': Configure only the z-axis
    # @param pct The sensitivity expressed as percentage.
    #   1. 0% = Shut down: Tap detection should not occur along the
    #      axis.
    #   2. 100% = Maximum sensitivity.
    def set_tap_sensitivity(self, axis='all', pct=50.0):
        axis = axis.lower()
        axis_c_int = c_int()
        if axis == 'x':
            axis_c_int = 0
        elif axis == 'y':
            axis_c_int = 1
        elif axis == 'z':
            axis_c_int = 2
        elif axis == 'all':
            axis_c_int = 3
        else:
            raise AssertionError('invalid input value ' + axis)
        ret = self._zkSetTapSensitivity(self._zk_ctx, axis_c_int, pct)
        if ret < 0:
            raise AssertionError('bad return code {!r}'.format(ret))

    ## @brief Get current GMT time
    #  @details This function is called to get the time directly from a
    #           Zymkey's Real Time Clock (RTC)
    # @param precise If true, this API returns the time after the next second
    #        falls. This means that the caller could be blocked up to one second.
    #        If false, the API returns immediately with the current time reading.
    # @returns The time in seconds from the epoch (Jan. 1, 1970)
    def get_time(self, precise=False):
        epoch_sec = c_int()
        ret = self._zkGetTime(self._zk_ctx, byref(epoch_sec), precise)
        if ret < 0:
            raise AssertionError('bad return code {!r}'.format(ret))
        return epoch_sec.value

    ## @brief Set current GMT time
    #  @details This function is called to set the RTC time to the system GMT time,
    #           similar to hwclock -w
    def set_GMT_time(self):
        ret = self._zkSetGMTTime(self._zk_ctx)
        if ret < 0:
            raise AssertionError('bad return code {!r}'.format(ret))

    ## @var Zymkey context instance, created during the __init__ of the
    #    class instance.
    _zk_ctx = c_void_p()

    # Interfaces to the C library
    _zkOpen = zkalib.zkOpen
    _zkOpen.restype = c_int
    _zkOpen.argtypes = [POINTER(c_void_p)]

    _zkLEDOn = zkalib.zkLEDOn
    _zkLEDOn.restype = c_int
    _zkLEDOn.argtypes = [c_void_p]

    _zkLEDOff = zkalib.zkLEDOff
    _zkLEDOff.restype = c_int
    _zkLEDOff.argtypes = [c_void_p]

    _zkLEDFlash = zkalib.zkLEDFlash
    _zkLEDFlash.restype = c_int
    _zkLEDFlash.argtypes = [c_void_p, c_ulong, c_ulong, c_ulong]

    _zkGetRandBytes = zkalib.zkGetRandBytes
    _zkGetRandBytes.restype = c_int
    _zkGetRandBytes.argtypes = [c_void_p, POINTER(c_void_p), c_int]

    _zkCreateRandDataFile = zkalib.zkCreateRandDataFile
    _zkCreateRandDataFile.restype = c_int
    _zkCreateRandDataFile.argtypes = (c_void_p, c_char_p, c_int)

    _zkLockDataF2F = zkalib.zkLockDataF2F
    _zkLockDataF2F.restype = c_int
    _zkLockDataF2F.argtypes = (c_void_p, c_char_p, c_char_p, c_bool)

    _zkLockDataB2F = zkalib.zkLockDataB2F
    _zkLockDataB2F.restype = c_int
    _zkLockDataB2F.argtypes = (c_void_p, c_void_p, c_int, c_char_p, c_bool)

    _zkLockDataF2B = zkalib.zkLockDataF2B
    _zkLockDataF2B.restype = c_int
    _zkLockDataF2B.argtypes = (c_void_p, c_char_p, POINTER(c_void_p), POINTER(c_int), c_bool)

    _zkLockDataB2B = zkalib.zkLockDataB2B
    _zkLockDataB2B.restype = c_int
    _zkLockDataB2B.argtypes = (c_void_p, c_void_p, c_int, POINTER(c_void_p), POINTER(c_int), c_bool)

    _zkUnlockDataF2F = zkalib.zkUnlockDataF2F
    _zkUnlockDataF2F.restype = c_int
    _zkUnlockDataF2F.argtypes = (c_void_p, c_char_p, c_char_p, c_bool)

    _zkUnlockDataB2F = zkalib.zkUnlockDataB2F
    _zkUnlockDataB2F.restype = c_int
    _zkUnlockDataB2F.argtypes = (c_void_p, c_void_p, c_int, c_char_p, c_bool)

    _zkUnlockDataF2B = zkalib.zkUnlockDataF2B
    _zkUnlockDataF2B.restype = c_int
    _zkUnlockDataF2B.argtypes = (c_void_p, c_char_p, POINTER(c_void_p), POINTER(c_int), c_bool)

    _zkUnlockDataB2B = zkalib.zkUnlockDataB2B
    _zkUnlockDataB2B.restype = c_int
    _zkUnlockDataB2B.argtypes = (c_void_p, c_void_p, c_int, POINTER(c_void_p), POINTER(c_int), c_bool)

    _zkGenECDSASigFromDigest = zkalib.zkGenECDSASigFromDigest
    _zkGenECDSASigFromDigest.restype = c_int
    _zkGenECDSASigFromDigest.argtypes = (c_void_p, c_void_p, c_int, POINTER(c_void_p), POINTER(c_int))

    _zkVerifyECDSASigFromDigest = zkalib.zkVerifyECDSASigFromDigest
    _zkVerifyECDSASigFromDigest.rettype = c_int
    _zkVerifyECDSASigFromDigest.argtypes = (c_void_p, c_void_p, c_int, c_void_p, c_int)

    _zkSaveECDSAPubKey2File = zkalib.zkSaveECDSAPubKey2File
    _zkSaveECDSAPubKey2File.restype = c_int
    _zkSaveECDSAPubKey2File.argtypes = (c_void_p, c_char_p, c_int)

    _zkGetECDSAPubKey = zkalib.zkGetECDSAPubKey
    _zkGetECDSAPubKey.restype = c_int
    _zkGetECDSAPubKey.argtypes = (c_void_p, POINTER(c_void_p), POINTER(c_int), c_int)

    _zkSetI2CAddr = zkalib.zkSetI2CAddr
    _zkSetI2CAddr.restype = c_int
    _zkSetI2CAddr.argtypes = (c_void_p, c_int)

    _zkSetTapSensitivity = zkalib.zkSetTapSensitivity
    _zkSetTapSensitivity.restype = c_int
    _zkSetTapSensitivity.argtypes = (c_void_p, c_int, c_float)

    _zkGetTime = zkalib.zkGetTime
    _zkGetTime.restype = c_int
    _zkGetTime.argtypes = (c_void_p, POINTER(c_int), c_bool)

    _zkSetGMTTime = zkalib.zkSetGMTTime
    _zkSetGMTTime.restype = c_int
    _zkSetGMTTime.argtypes = [c_void_p]
