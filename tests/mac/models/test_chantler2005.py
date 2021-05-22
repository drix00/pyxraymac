#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.mac.models.test_chantler2005
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`xray.mac.models.chantler2005` module.
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
from xray.mac import get_current_module_path
from xray.mac.models.chantler2005 import Chantler2005, ENERGIES_eV, MAC_cm2_g, ENERGY_UNIT_eV

# Globals and constants variables.


class TestChantler2005(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        # self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_read_mac_data(self):
        file_path = get_current_module_path(__file__, "../../../data/chantler2005/FFastMAC.csv")

        mac = Chantler2005()
        mac.read_mac_data(file_path)

        self.assertEquals(92, len(mac.experimental_data))

        atomic_number = 1
        energies_eV = mac.experimental_data[atomic_number][ENERGIES_eV]
        mac_cm2_g = mac.experimental_data[atomic_number][MAC_cm2_g]

        self.assertAlmostEquals(0.013668*1.0e3, energies_eV[0])
        self.assertAlmostEquals(2907600.0, mac_cm2_g[0])

        self.assertAlmostEquals(432.9451*1.0e3, energies_eV[-1])
        self.assertAlmostEquals(0.0000000088048, mac_cm2_g[-1])

        atomic_number = 92
        energies_eV = mac.experimental_data[atomic_number][ENERGIES_eV]
        mac_cm2_g = mac.experimental_data[atomic_number][MAC_cm2_g]

        self.assertAlmostEquals(0.0324615*1.0e3, energies_eV[0])
        self.assertAlmostEquals(43925.0, mac_cm2_g[0])

        self.assertAlmostEquals(432.9451*1.0e3, energies_eV[-1])
        self.assertAlmostEquals(0.15459, mac_cm2_g[-1])

    def test_read_mac_data_dtsa2(self):
        file_path = get_current_module_path(__file__, "../../../data/chantler2005/FFastMAC_DTSA2.csv")

        mac = Chantler2005()
        mac.read_mac_data(file_path)

        self.assertEquals(92, len(mac.experimental_data))

        atomic_number = 1
        energies_eV = mac.experimental_data[atomic_number][ENERGIES_eV]
        mac_cm2_g = mac.experimental_data[atomic_number][MAC_cm2_g]

        self.assertAlmostEquals(0.013668*1.0e3, energies_eV[0])
        self.assertAlmostEquals(2907600.0, mac_cm2_g[0])

        self.assertAlmostEquals(432.9451*1.0e3, energies_eV[-1])
        self.assertAlmostEquals(0.0000000088048, mac_cm2_g[-1])

        atomic_number = 92
        energies_eV = mac.experimental_data[atomic_number][ENERGIES_eV]
        mac_cm2_g = mac.experimental_data[atomic_number][MAC_cm2_g]

        self.assertAlmostEquals(0.0324615*1.0e3, energies_eV[0])
        self.assertAlmostEquals(43925.0, mac_cm2_g[0])

        self.assertAlmostEquals(432.9451*1.0e3, energies_eV[-1])
        self.assertAlmostEquals(0.15459, mac_cm2_g[-1])

    def test_read_mac_data_NISTMonte2(self):
        file_path = get_current_module_path(__file__, "../../../data/chantler2005/FFastMAC_nistMonte2.csv")

        mac = Chantler2005()
        mac.read_mac_data(file_path, ENERGY_UNIT_eV)

        self.assertEquals(92, len(mac.experimental_data))

        atomic_number = 1
        energies_eV = mac.experimental_data[atomic_number][ENERGIES_eV]
        mac_cm2_g = mac.experimental_data[atomic_number][MAC_cm2_g]

        self.assertAlmostEquals(10.69, energies_eV[0])
        self.assertAlmostEquals(0.22129, mac_cm2_g[0])

        self.assertAlmostEquals(432945.1, energies_eV[-1])
        self.assertAlmostEquals(0.1753, mac_cm2_g[-1])

        atomic_number = 92
        energies_eV = mac.experimental_data[atomic_number][ENERGIES_eV]
        mac_cm2_g = mac.experimental_data[atomic_number][MAC_cm2_g]

        self.assertAlmostEquals(10.69, energies_eV[0])
        self.assertAlmostEquals(0.00012189, mac_cm2_g[0])

        self.assertAlmostEquals(432945.1, energies_eV[-1])
        self.assertAlmostEquals(0.23698, mac_cm2_g[-1])

    def test_default_data_files(self):
        mac = Chantler2005()
        mac.read_mac_data()

        self.assertEquals(92, len(mac.experimental_data))

        atomic_number = 1
        energies_eV = mac.experimental_data[atomic_number][ENERGIES_eV]
        mac_cm2_g = mac.experimental_data[atomic_number][MAC_cm2_g]

        self.assertAlmostEquals(0.013668*1.0e3, energies_eV[0])
        self.assertAlmostEquals(2907600.0, mac_cm2_g[0])

        self.assertAlmostEquals(432.9451*1.0e3, energies_eV[-1])
        self.assertAlmostEquals(0.0000000088048, mac_cm2_g[-1])

        atomic_number = 92
        energies_eV = mac.experimental_data[atomic_number][ENERGIES_eV]
        mac_cm2_g = mac.experimental_data[atomic_number][MAC_cm2_g]

        self.assertAlmostEquals(0.0324615*1.0e3, energies_eV[0])
        self.assertAlmostEquals(43925.0, mac_cm2_g[0])

        self.assertAlmostEquals(432.9451*1.0e3, energies_eV[-1])
        self.assertAlmostEquals(0.15459, mac_cm2_g[-1])

    def test_compute_mac_cm2_g(self):
        chantler2005 = Chantler2005()

        atomic_number = 1
        energy_eV = 13.7
        mac_cm2_g = chantler2005.compute_mac_cm2_g(energy_eV, atomic_number)
        self.assertAlmostEquals(2890658.8235294116, mac_cm2_g)

        energy_eV = 14.0
        mac_cm2_g = chantler2005.compute_mac_cm2_g(energy_eV, atomic_number)
        self.assertAlmostEquals(2736735.1622112636, mac_cm2_g)

        energy_eV = 14.8
        mac_cm2_g = chantler2005.compute_mac_cm2_g(energy_eV, atomic_number)
        self.assertAlmostEquals(2376537.9133143006, mac_cm2_g)

        energy_eV = 1000.0
        mac_cm2_g = chantler2005.compute_mac_cm2_g(energy_eV, atomic_number)
        self.assertAlmostEquals(6.924559683551284, mac_cm2_g)
