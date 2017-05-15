# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import copy
from diskimage_builder.block_device.level0.localloop import LocalLoop
from diskimage_builder.block_device.level1.mbr import MBR
from diskimage_builder.logging_config import setup
import logging
import os
import shutil
import subprocess
import tempfile
import testtools


class TestMBR(testtools.TestCase):

    disk_size_10M = 10 * 1024 * 1024
    disk_size_1G = 1024 * 1024 * 1024

    pargs = ["--raw", "--output",
             "NR,START,END,TYPE,FLAGS,SCHEME", "-g", "-b", "-"]

    def _get_path_for_partx(self):
        """Searches and sets the path for partx

        Because different distributions store the partx binary
        at different places, there is the need to look for it.
        """

        dirs = ["/bin", "/usr/bin", "/sbin", "/usr/sbin"]

        for d in dirs:
            if os.path.exists(os.path.join(d, "partx")):
                return os.path.join(d, "partx")
                return
        # If not found, try without path.
        return "partx"

    def setUp(self):
        super(TestMBR, self).setUp()
        setup()

    def _create_image(self):
        tmp_dir = tempfile.mkdtemp(prefix="dib-bd-mbr-")
        image_path = os.path.join(tmp_dir, "image.raw")
        LocalLoop.image_create(image_path, TestMBR.disk_size_1G)
        return tmp_dir, image_path

    def _run_partx(self, image_path):
        largs = copy.copy(TestMBR.pargs)
        partx_path = self._get_path_for_partx()
        largs.insert(0, partx_path)
        largs.append(image_path)
        logging.info("Running command [%s]", largs)
        return subprocess.check_output(largs).decode("ascii")

    def test_one_ext_partition(self):
        """Creates one partition and check correctness with partx."""

        tmp_dir, image_path = self._create_image()
        with MBR(image_path, TestMBR.disk_size_1G, 1024 * 1024) as mbr:
            mbr.add_partition(False, False, TestMBR.disk_size_10M, 0x83)

        output = self._run_partx(image_path)
        shutil.rmtree(tmp_dir)
        self.assertEqual(
            "1 2048 2097151 0xf 0x0 dos\n"
            "5 4096 24575 0x83 0x0 dos\n", output)

    def test_zero_partitions(self):
        """Creates no partition and check correctness with partx."""

        tmp_dir, image_path = self._create_image()
        with MBR(image_path, TestMBR.disk_size_1G, 1024 * 1024):
            pass

        output = self._run_partx(image_path)
        shutil.rmtree(tmp_dir)
        self.assertEqual("", output)

    def test_many_ext_partitions(self):
        """Creates many partition and check correctness with partx."""

        tmp_dir, image_path = self._create_image()
        with MBR(image_path, TestMBR.disk_size_1G, 1024 * 1024) as mbr:
            for nr in range(0, 64):
                mbr.add_partition(False, False, TestMBR.disk_size_10M, 0x83)

        output = self._run_partx(image_path)

        shutil.rmtree(tmp_dir)

        lines = output.split("\n")
        self.assertEqual(66, len(lines))

        self.assertEqual(
            "1 2048 2097151 0xf 0x0 dos", lines[0])

        start_block = 4096
        end_block = start_block + TestMBR.disk_size_10M / 512 - 1
        for nr in range(1, 65):
            fields = lines[nr].split(" ")
            self.assertEqual(6, len(fields))
            self.assertEqual(nr + 4, int(fields[0]))
            self.assertEqual(start_block, int(fields[1]))
            self.assertEqual(end_block, int(fields[2]))
            self.assertEqual("0x83", fields[3])
            self.assertEqual("0x0", fields[4])
            self.assertEqual("dos", fields[5])
            start_block += 22528
            end_block = start_block + TestMBR.disk_size_10M / 512 - 1

    def test_one_pri_partition(self):
        """Creates one primary partition and check correctness with partx."""

        tmp_dir, image_path = self._create_image()
        with MBR(image_path, TestMBR.disk_size_1G, 1024 * 1024) as mbr:
            mbr.add_partition(True, False, TestMBR.disk_size_10M, 0x83)

        output = self._run_partx(image_path)
        shutil.rmtree(tmp_dir)
        self.assertEqual(
            "1 2048 22527 0x83 0x0 dos\n", output)

    def test_three_pri_partition(self):
        """Creates three primary partition and check correctness with partx."""

        tmp_dir, image_path = self._create_image()
        with MBR(image_path, TestMBR.disk_size_1G, 1024 * 1024) as mbr:
            for _ in range(3):
                mbr.add_partition(True, False, TestMBR.disk_size_10M, 0x83)

        output = self._run_partx(image_path)
        shutil.rmtree(tmp_dir)
        self.assertEqual(
            "1 2048 22527 0x83 0x0 dos\n"
            "2 22528 43007 0x83 0x0 dos\n"
            "3 43008 63487 0x83 0x0 dos\n", output)

    def test_many_pri_and_ext_partition(self):
        """Creates many primary and extended partitions."""

        tmp_dir, image_path = self._create_image()
        with MBR(image_path, TestMBR.disk_size_1G, 1024 * 1024) as mbr:
            # Create three primary partitions
            for _ in range(3):
                mbr.add_partition(True, False, TestMBR.disk_size_10M, 0x83)
            for _ in range(7):
                mbr.add_partition(False, False, TestMBR.disk_size_10M, 0x83)

        output = self._run_partx(image_path)
        shutil.rmtree(tmp_dir)
        self.assertEqual(
            "1 2048 22527 0x83 0x0 dos\n"     # Primary 1
            "2 22528 43007 0x83 0x0 dos\n"    # Primary 2
            "3 43008 63487 0x83 0x0 dos\n"    # Primary 3
            "4 63488 2097151 0xf 0x0 dos\n"   # Extended
            "5 65536 86015 0x83 0x0 dos\n"    # Extended Partition 1
            "6 88064 108543 0x83 0x0 dos\n"   # Extended Partition 2
            "7 110592 131071 0x83 0x0 dos\n"  # ...
            "8 133120 153599 0x83 0x0 dos\n"
            "9 155648 176127 0x83 0x0 dos\n"
            "10 178176 198655 0x83 0x0 dos\n"
            "11 200704 221183 0x83 0x0 dos\n", output)
