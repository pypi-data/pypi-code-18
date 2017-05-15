# coding: utf-8

from __future__ import division, print_function, unicode_literals, absolute_import

import json
import os
import shutil
import unittest

import numpy as np

from pymongo import MongoClient

from fireworks import LaunchPad, FWorker
from fireworks.core.rocket_launcher import rapidfire

from atomate.vasp.powerups import use_fake_vasp
from atomate.vasp.workflows.presets.core import wf_raman_spectra

from pymatgen import SETTINGS
from pymatgen.util.testing import PymatgenTest

__author__ = 'Kiran Mathew'
__email__ = 'kmathew@lbl.gov'

module_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
db_dir = os.path.join(module_dir, "..", "..", "..", "common", "test_files")
ref_dir = os.path.join(module_dir, "..", "..", "test_files")

DEBUG_MODE = False  # If true, retains the database and output dirs at the end of the test
VASP_CMD = None  # If None, runs a "fake" VASP. Otherwise, runs VASP with this command...


class TestRamanWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not SETTINGS.get("PMG_VASP_PSP_DIR"):
            SETTINGS["PMG_VASP_PSP_DIR"] = os.path.join(module_dir, "..", "..", "tests", "..", "..", "test_files")
            print('This system is not set up to run VASP jobs. '
                  'Please set PMG_VASP_PSP_DIR variable in your ~/.pmgrc.yaml file.')

        cls.struct_si = PymatgenTest.get_structure("Si")
        cls.scratch_dir = os.path.join(module_dir, "scratch")
        cls.raman_config = {"modes": [0, 1], "step_size": 0.005,
                            "vasp_cmd": ">>vasp_cmd<<", "db_file": ">>db_file<<"}
        cls.wf = wf_raman_spectra(cls.struct_si, cls.raman_config)

    def setUp(self):
        if os.path.exists(self.scratch_dir):
            shutil.rmtree(self.scratch_dir)
        os.makedirs(self.scratch_dir)
        os.chdir(self.scratch_dir)
        try:
            self.lp = LaunchPad.from_file(os.path.join(db_dir, "my_launchpad.yaml"))
            self.lp.reset("", require_password=False)
        except:
            raise unittest.SkipTest(
                'Cannot connect to MongoDB! Is the database server running? '
                'Are the credentials correct?')

    def tearDown(self):
        if not DEBUG_MODE:
            shutil.rmtree(self.scratch_dir)
            self.lp.reset("", require_password=False)
            db = self._get_task_database()
            for coll in db.collection_names():
                if coll != "system.indexes":
                    db[coll].drop()
            os.chdir(module_dir)

    def _simulate_vasprun(self, wf):
        reference_dir = os.path.abspath(os.path.join(ref_dir, "raman_wf"))
        si_ref_dirs = {"structure optimization": os.path.join(reference_dir, "1"),
                       "phonon static dielectric": os.path.join(reference_dir, "2"),
                       "raman_0_-0.005 static dielectric": os.path.join(reference_dir, "6"),
                       "raman_0_0.005 static dielectric": os.path.join(reference_dir, "5"),
                       "raman_1_-0.005 static dielectric": os.path.join(reference_dir, "4"),
                       "raman_1_0.005 static dielectric": os.path.join(reference_dir, "3")}
        return use_fake_vasp(wf, si_ref_dirs, params_to_check=["ENCUT"])

    def _get_task_database(self):
        with open(os.path.join(db_dir, "db.json")) as f:
            creds = json.loads(f.read())
            conn = MongoClient(creds["host"], creds["port"])
            db = conn[creds["database"]]
            if "admin_user" in creds:
                db.authenticate(creds["admin_user"], creds["admin_password"])
            return db

    def _get_task_collection(self, coll_name=None):
        with open(os.path.join(db_dir, "db.json")) as f:
            creds = json.loads(f.read())
            db = self._get_task_database()
            coll_name = coll_name or creds["collection"]
            return db[coll_name]

    def _check_run(self, d, mode):
        if mode not in ["structure optimization", "phonon static dielectric",
                        "raman_0_0.005 static dielectric", "raman analysis"]:
            raise ValueError("Invalid mode!")

        if mode not in ["raman analysis"]:
            self.assertEqual(d["formula_pretty"], "Si")
            self.assertEqual(d["formula_anonymous"], "A")
            self.assertEqual(d["nelements"], 1)
            self.assertEqual(d["state"], "successful")
            self.assertAlmostEqual(d["calcs_reversed"][0]["output"]["structure"]["lattice"]["a"], 3.867, 2)

        if mode in ["structure optimization"]:
            self.assertAlmostEqual(d["output"]["energy"], -10.850, 2)
            self.assertAlmostEqual(d["output"]["energy_per_atom"], -5.425, 2)

        elif mode in ["phonon static dielectric"]:
            epsilon = [[13.23245131, -1.98e-06, -1.4e-06],
                       [-1.98e-06, 13.23245913, 8.38e-06],
                       [-1.4e-06, 8.38e-06, 13.23245619]]
            np.testing.assert_allclose(epsilon, d["output"]["epsilon_static"], rtol=1e-5)

        elif mode in ["raman_0_0.005 static dielectric"]:
            epsilon = [[13.16509632, 0.00850098, 0.00597267],
                       [0.00850097, 13.25477303, -0.02979572],
                       [0.00597267, -0.0297953, 13.28883867]]
            np.testing.assert_allclose(epsilon, d["output"]["epsilon_static"], rtol=1e-5)

        elif mode in ["raman analysis"]:
            freq = [82.13378641656142, 82.1337379843688, 82.13373236539397,
                    3.5794336040310436e-07, 3.872360276932139e-07, 1.410955723105983e-06]
            np.testing.assert_allclose(freq, d["frequencies"], rtol=1e-5)
            raman_tensor = {'0': [[-0.14893062387265346, 0.01926196125448702, 0.013626954435454657],
                                  [0.019262321540910236, 0.03817444467845385, -0.06614541890150054],
                                  [0.013627229948601821, -0.06614564143135017, 0.11078513986463052]],
                            '1': [[-0.021545749071077102, -0.12132200642389818, -0.08578776196143767],
                                  [-0.12131975993142007, -0.00945267872479081, -0.004279822490713417],
                                  [-0.08578678706847546, -0.004279960247327641, 0.032660281203217366]]}
            np.testing.assert_allclose(raman_tensor["0"], d["raman_tensor"]["0"], rtol=1e-5)
            np.testing.assert_allclose(raman_tensor["1"], d["raman_tensor"]["1"], rtol=1e-5)

    def test_wf(self):
        self.wf = self._simulate_vasprun(self.wf)

        self.assertEqual(len(self.wf.fws), len(self.raman_config["modes"]) * 2 + 3)

        self.lp.add_wf(self.wf)
        rapidfire(self.lp, fworker=FWorker(env={"db_file": os.path.join(db_dir, "db.json")}))

        # check relaxation
        d = self._get_task_collection().find_one({"task_label": "structure optimization"})
        self._check_run(d, mode="structure optimization")

        # check phonon DFPT calculation
        d = self._get_task_collection().find_one({"task_label": "phonon static dielectric"})
        self._check_run(d, mode="phonon static dielectric")

        # check one of the raman static dielectric calculation
        d = self._get_task_collection().find_one({"task_label": "raman_0_0.005 static dielectric"})
        self._check_run(d, mode="raman_0_0.005 static dielectric")

        # check the final results
        d = self._get_task_collection(coll_name="raman").find_one()
        self._check_run(d, mode="raman analysis")

        wf = self.lp.get_wf_by_fw_id(1)
        self.assertTrue(all([s == 'COMPLETED' for s in wf.fw_states.values()]))


if __name__ == "__main__":
    unittest.main()
