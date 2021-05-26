#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.mac.models.test_casino
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`xray.mac.models.casino` module.
"""

###############################################################################
# Copyright 2021 Hendrix Demers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

# Standard library modules.
import unittest

# Third party modules.

# Local modules.

# Project modules.
from xray.mac.models.casino import mac_zaluzec_cm2_g, MACSTOTAL, MACS_HENKE_EBISU, EFFICACITE, MACS_HEINRICH, \
    SPECIAL_EQUATIONS

# Globals and constants variables.


class TestCasino(unittest.TestCase):
    """
    TestCase class for the module `casino`.
    """

    def setUp(self):
        """
        Setup method.
        """

        unittest.TestCase.setUp(self)

    def tearDown(self):
        """
        Teardown method.
        """

        unittest.TestCase.tearDown(self)

    def test_skeleton(self):
        """
        First test to check if the testcase is working with the testing framework.
        """

        # self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_mac_zaluzec_cm2_g(self):
        """
        Tests for method `mac_zaluzec_cm2_g`.
        """

        mac_ref_cm2_g = 837938.9116018773
        atomic_number = 13
        wavelength_A = 202.854347826  # noqa
        mac_cm2_g = mac_zaluzec_cm2_g(wavelength_A, atomic_number)
        self.assertAlmostEqual(mac_ref_cm2_g, mac_cm2_g)

        atomic_number = 6
        macs_ref_cm2_g = {0.1: 2.238906023607424,
                          0.2: 5236.252721312064,
                          0.5: 13875.379755662734,
                          1.0: 2197.1394891008304,
                          5.0: 18.516130819039912,
                          10.0: 2.2522353140592553}

        energies_keV = sorted(macs_ref_cm2_g.keys())  # noqa
        for energy_keV in energies_keV:
            wavelength_A = 12.3981/energy_keV  # noqa
            mac_cm2_g = mac_zaluzec_cm2_g(wavelength_A, atomic_number)
            self.assertAlmostEqual(macs_ref_cm2_g[energy_keV], mac_cm2_g, msg=energy_keV)

        atomic_number = 4
        macs_ref_cm2_g = {0.1: 315647.0180940999,
                          0.2: 48688.995956979,
                          0.5: 4483.888675972408,
                          1.0: 592.6530904778803,
                          5.0: 3.7734188099041619,
                          10.0: 0.39670107324940557}

        energies_keV = sorted(macs_ref_cm2_g.keys())  # noqa
        for energy_keV in energies_keV:
            wavelength_A = 12.3981/energy_keV  # noqa
            mac_cm2_g = mac_zaluzec_cm2_g(wavelength_A, atomic_number)
            self.assertAlmostEqual(macs_ref_cm2_g[energy_keV], mac_cm2_g, msg=energy_keV)

        atomic_number = 79
        macs_ref_cm2_g = {0.1: 14554.743378487043,
                          0.2: 10578.75966994802,
                          0.5: 12522.008361485307,
                          1.0: 4994.772986063444,
                          5.0: 702.60382519274265,
                          10.0: 115.75123581861371}

        energies_keV = sorted(macs_ref_cm2_g.keys())  # noqa
        for energy_keV in energies_keV:
            wavelength_A = 12.3981/energy_keV  # noqa
            mac_cm2_g = mac_zaluzec_cm2_g(wavelength_A, atomic_number)
            self.assertAlmostEqual(macs_ref_cm2_g[energy_keV], mac_cm2_g, msg=energy_keV)

    def compare_mac(self, mac_ref_cm2_g, atomic_number):
        energies_keV = sorted(mac_ref_cm2_g.keys())  # noqa
        for energie_keV in energies_keV:  # noqa
            mac_cm2_g = SPECIAL_EQUATIONS(energie_keV, atomic_number)
            if mac_cm2_g is not None:
                self.assertAlmostEqual(mac_ref_cm2_g[energie_keV], mac_cm2_g, msg=energie_keV)
            else:
                self.assertEqual(None, mac_cm2_g, msg=energie_keV)

    def test_special_equations(self):
        """
        Tests for method `SPECIAL_EQUATIONS`.
        """

        atomic_number = 1
        mac_ref_cm2_g = {0.1: 0.0,
                         0.5: 0.0,
                         1.0: 3.1489416039958913,
                         1.45: 3.1319053886995225,
                         1.487: 3.1307534420695196,
                         1.5: 3.130355596071175,
                         3.0: 3.805083748684189,
                         3.9: 3.814242686635657,
                         5.0: 3.780274124237171,
                         9.0: 0.7180027252958251,
                         10.0: 0.09799012234499979,
                         50.0: 0.0}

        self.compare_mac(mac_ref_cm2_g, atomic_number)

        atomic_number = 2
        mac_ref_cm2_g = {1.0: 3.9559633687657905,
                         5.0: 4.0556664414604,
                         8.0: 2.6625877400897426,
                         15.0: 1.0822687002197757,
                         30.0: 0.07350235898200384,
                         50.0: 0.0}

        self.compare_mac(mac_ref_cm2_g, atomic_number)

        atomic_number = 3
        mac_ref_cm2_g = {5.0: 5.2947017843354764,
                         7.0: 6.548121479457815,
                         12.0: 4.207136721849756,
                         15.0: 1.8826527366391121,
                         30.0: 0.23913760241931142,
                         50.0: 0.0}

        self.compare_mac(mac_ref_cm2_g, atomic_number)

        atomic_number = 4
        mac_ref_cm2_g = {5.0: 7.845115390997546,
                         12.0: 8.10163078475115,
                         15.0: 5.146632275325647,
                         30.0: 0.4878487401767469,
                         50.0: 0.0}

        self.compare_mac(mac_ref_cm2_g, atomic_number)

        atomic_number = 5
        mac_ref_cm2_g = {10.0: 7.622129191433776,
                         12.0: 10.411543612467906,
                         20.0: 5.39078010,
                         30.0: 2.68378122,
                         35.0: 0.0,
                         50.0: 0.42022409}

        self.compare_mac(mac_ref_cm2_g, atomic_number)

        atomic_number = 6
        mac_ref_cm2_g = {10.0: 11.68225651,
                         20.0: 7.64629861,
                         25.0: 5.89155229,
                         30.0: 1.80234908,
                         50.0: 0.0}

        self.compare_mac(mac_ref_cm2_g, atomic_number)

        atomic_number = 7
        mac_ref_cm2_g = {10.0: 16.29504405,
                         20.0: 7.44826745,
                         25.0: 6.14576204,
                         35.0: 3.36012704,
                         50.0: 0.0}

        self.compare_mac(mac_ref_cm2_g, atomic_number)

        atomic_number = 8
        mac_ref_cm2_g = {10.0: 16.63414006,
                         22.0: 6.00639700,
                         38.0: 3.97868026,
                         50.0: 0.0}

        self.compare_mac(mac_ref_cm2_g, atomic_number)

        atomic_number = 9
        mac_ref_cm2_g = {10.0: 19.22812814,
                         28.0: 2.78975738,
                         38.0: 3.87790122,
                         50.0: 0.0}

        self.compare_mac(mac_ref_cm2_g, atomic_number)

        atomic_number = 10
        mac_ref_cm2_g = {10.0: 29.22233616,
                         28.0: 1.58866175,
                         38.0: 2.66238021,
                         50.0: 0.0}

        self.compare_mac(mac_ref_cm2_g, atomic_number)

        atomic_number = 11
        mac_ref_cm2_g = {10.0: 53.23487856,
                         28.0: 4.22422595,
                         38.0: 2.25585760,
                         50.0: 0.0}

        self.compare_mac(mac_ref_cm2_g, atomic_number)

        atomic_number = 12
        mac_ref_cm2_g = {10.0: 0.0,
                         28.0: 2.02211034,
                         50.0: 0.0}

        self.compare_mac(mac_ref_cm2_g, atomic_number)

        atomic_number = 13
        mac_ref_cm2_g = {10.0: 0.0,
                         38.0: 0.64809106,
                         50.0: 0.0}

        self.compare_mac(mac_ref_cm2_g, atomic_number)

        atomic_number = 14
        mac_ref_cm2_g = {10.0: 0.0,
                         38.0: 0.13414860,
                         50.0: 0.0}

        self.compare_mac(mac_ref_cm2_g, atomic_number)

        atomic_number = 15
        mac_ref_cm2_g = {10.0: 118.27759319,
                         38.0: 0.0,
                         50.0: 0.0}

        self.compare_mac(mac_ref_cm2_g, atomic_number)

        atomic_number = 16
        mac_ref_cm2_g = {10.0: 0.0,
                         38.0: 0.04083431,
                         50.0: 0.0}

        self.compare_mac(mac_ref_cm2_g, atomic_number)

    def test_macs_henke_ebisu(self):
        """
        Tests for method `MACS_HENKE_EBISU`.
        """

        atomic_number = 6
        mac_ref_cm2_g = {0.1: 2.238906023607424,
                         0.5: 14290.95890410959,
                         1.0: 2229.9756097560976,
                         1.5: -1227.3414634146357,
                         5.0: -1.0,
                         10.0: -1.0}

        energies_keV = sorted(mac_ref_cm2_g.keys())  # noqa
        for energy_keV in energies_keV:  # noqa
            mac_cm2_g = MACS_HENKE_EBISU(energy_keV, atomic_number)
            self.assertAlmostEqual(mac_ref_cm2_g[energy_keV], mac_cm2_g, msg=energy_keV)

        mac_ref_cm2_g = 3.7542043000041594
        atomic_number = 1
        energy_keV = 1.2  # noqa
        mac_cm2_g = MACS_HENKE_EBISU(energy_keV, atomic_number)
        self.assertAlmostEqual(mac_ref_cm2_g, mac_cm2_g)

        mac_ref_cm2_g = -1.0
        atomic_number = 2
        energy_keV = 1.2  # noqa
        mac_cm2_g = MACS_HENKE_EBISU(energy_keV, atomic_number)
        self.assertAlmostEqual(mac_ref_cm2_g, mac_cm2_g)

        mac_ref_cm2_g = -1.0
        atomic_number = 96
        energy_keV = 1.2  # noqa
        mac_cm2_g = MACS_HENKE_EBISU(energy_keV, atomic_number)
        self.assertAlmostEqual(mac_ref_cm2_g, mac_cm2_g)

    def test_macs_total(self):
        """
        Tests for method `MACS_TOTAL`.
        """

        atomic_number = 6
        mac_ref_cm2_g = {0.1: 2.238906023607424,
                         0.5: 14290.95890410959,
                         1.0: 2229.9756097560976,
                         5.0: 18.516130819039919,
                         10.0: 2.2522353140592566}

        energies_keV = sorted(mac_ref_cm2_g.keys())  # noqa
        for energie_keV in energies_keV:  # noqa
            mac_cm2_g = MACSTOTAL(energie_keV, atomic_number)
            self.assertAlmostEqual(mac_ref_cm2_g[energie_keV], mac_cm2_g, msg=energie_keV)

        self.assertRaises(ValueError, MACSTOTAL, 0.0, 1)
        self.assertRaises(ValueError, MACSTOTAL, 0.0, 2)

    def test_macs_heinrich(self):
        """
        Tests for method `MACS_HEINRICH`.
        """

        atomic_number = 6
        mac_ref_cm2_g = {0.1: 23229.785089103985,
                         0.5: 13062.690142874741,
                         1.0: 2154.0465317987741,
                         5.0: 18.516130819039919,
                         10.0: 2.2522353140592566}

        energies_keV = sorted(mac_ref_cm2_g.keys())  # noqa
        for energy_keV in energies_keV:  # noqa
            wavelength_A = 12.3981/energy_keV  # noqa
            mac_cm2_g = MACS_HEINRICH(wavelength_A, atomic_number)
            self.assertAlmostEqual(mac_ref_cm2_g[energy_keV], mac_cm2_g, msg=energy_keV)

        mac_ref_cm2_g = 375.07124151210633
        atomic_number = 4
        energy_keV = 1.2  # noqa
        wavelength_A = 12.3981 / energy_keV  # noqa
        mac_cm2_g = MACS_HEINRICH(wavelength_A, atomic_number)
        self.assertAlmostEqual(mac_ref_cm2_g, mac_cm2_g)

        atomic_number = 29
        mac_ref_cm2_g = {5.0: 195.45892003851989,
                         1.0: 10376.703975399581,
                         0.940: 9826.5361934375778,
                         0.900: 1699.549897374447,
                         }

        energies_keV = sorted(mac_ref_cm2_g.keys())  # noqa
        for energy_keV in energies_keV:
            wavelength_A = 12.3981/energy_keV  # noqa
            mac_cm2_g = MACS_HEINRICH(wavelength_A, atomic_number)
            self.assertAlmostEqual(mac_ref_cm2_g[energy_keV], mac_cm2_g, msg=energy_keV)

        atomic_number = 79
        mac_ref_cm2_g = {85.0: 3276.5609362875975,
                         15.0: 161.4269786327917,
                         14.0: 164.91858879982485,
                         12.0: 179.97622524730096,
                         10.0: 115.75123581861376,
                         8.0: 208.82276414451934,
                         3.2: 1943.1293004850916,
                         3.0: 2072.741637102265,
                         2.5: 2699.4523561323849,
                         2.28: 1419.1729654572405,
                         1.0: 4971.5179929826181,
                         0.7: -0.0069754096032754705,
                         0.6: -0.005703876918824651,
                         0.5: -0.0044323442343738306,
                         0.34: -0.0023978919392525196,
                         0.2: -0.00061774618102137168
                         }

        energies_keV = sorted(mac_ref_cm2_g.keys())  # noqa
        for energy_keV in energies_keV:
            wavelength_A = 12.3981/energy_keV  # noqa
            mac_cm2_g = MACS_HEINRICH(wavelength_A, atomic_number)
            self.assertAlmostEqual(mac_ref_cm2_g[energy_keV], mac_cm2_g, msg=energy_keV)

    def test_efficiency(self):
        """
        Tests for method `EFFICACITE`.
        """

        efficiencies_ref = {0.02: 0.0,
                            0.03: 0.0,
                            0.04: 1.4903443371725154e-46,
                            0.05: 1.8918833134077883e-28,
                            0.1: 1.441828924258387e-06,
                            0.5: 0.5305310049365957,
                            1.0: 0.8672380841993212,
                            5.0: 0.9899314637720737,
                            7.0: 1.0,
                            10.0: 1.0,
                            15.0: 1.0,
                            20.0: 0.9543591372789866,
                            30.0: 0.6078814863135107}

        energies_keV = sorted(efficiencies_ref.keys())  # noqa
        for energy_keV in energies_keV:
            efficiency = EFFICACITE(energy_keV)
            self.assertAlmostEqual(efficiencies_ref[energy_keV], efficiency, msg=energy_keV)
