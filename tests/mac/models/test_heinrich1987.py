#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.mac.models.test_heinrich1987
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`xray_mac.mac.models.heinrich1987` module.
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
import numpy as np

from xray_mac.mac.models.heinrich1987 import MacHeinrich1987
from xray_mac.mac.models.ionization_energies import IonizationEnergiesDtsa


# Globals and constants variables.


class TestMacHeinrich1987(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.heinrich1987 = MacHeinrich1987()
        self.heinrich1987.ionization_energies = IonizationEnergiesDtsa()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_skeleton(self):
        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def test_absorber_boron(self):
        """
        Test energy region 1, Z < 6.

        """
        macs_cm2_g = {183.0: 2861.0, 277.0: 39838.0}

        atomic_number_absorber = 5

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

            self.assertAlmostEqual(macs_cm2_g[energy_eV], mac_cm2_g, 0)

    def test_absorber_carbon(self):
        """
        Test energy region 1, Z > 5.

        """
        macs_cm2_g = {183.0: 5945.0, 277.0: 2147.0, 392.0: 23586.0}

        atomic_number_absorber = 6

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

            self.assertAlmostEqual(macs_cm2_g[energy_eV], mac_cm2_g, 0)

    #        data_mac_cm2_g = self.heinrich1987.mac_cm2_g(energy_eV, atomicNumberAbsorber)

    def test_region2(self):
        """
        Test energy region 2.

        """
        macs_cm2_g = {2014.0: 2238.0, 8048.0: 52.4}

        atomic_number_absorber = 29

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

            self.assertAlmostEqual(macs_cm2_g[energy_eV], mac_cm2_g, 0)

    def test_region3(self):
        """
        Test energy region 3.

        """
        macs_cm2_g = {3692.0: 1409.0, 3590.0: 1508.7}

        atomic_number_absorber = 47

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

            self.assertAlmostEqual(macs_cm2_g[energy_eV], mac_cm2_g, 0)

    def test_region4(self):
        """
        Test energy region 4.

        """
        macs_cm2_g = {3444.0: 1254.0, 3487.0: 1217.0}

        atomic_number_absorber = 47

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

            self.assertAlmostEqual(macs_cm2_g[energy_eV], mac_cm2_g, 0)

    def test_absorber_copper(self):
        """
        Test energy region 5, Z < 30.

        """
        macs_cm2_g = {183.0: 37113.3, 277.0: 19141.5, 392.0: 9925.8}

        atomic_number_absorber = 29

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

            self.assertAlmostEqual(macs_cm2_g[energy_eV], mac_cm2_g, 0)

    def test_mac_vector(self):
        """
        Test energy region 5, Z < 30.

        """
        energies_eV = np.array([183.0, 277.0, 392.0])
        macs_ref_cm2_g = np.array([37113.31949492, 19141.49605365,  9925.82401593])

        atomic_number_absorber = 29

        macs_cm2_g = self.heinrich1987.compute_mac_cm2_g(energies_eV, atomic_number_absorber)

        np.testing.assert_allclose(macs_ref_cm2_g, macs_cm2_g)

    def test_absorber_zinc(self):
        """
        Test energy region 5, Z > 29.

        """
        macs_cm2_g = {183.0: 40790.1, 277.0: 21582.7, 392.0: 11317.3}

        atomic_number_absorber = 30

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

            self.assertAlmostEqual(macs_cm2_g[energy_eV], mac_cm2_g, 0)

    def test_absorber_neodymium(self):
        """
        Test energy region 5, Z < 61.

        """
        macs_cm2_g = {1740.0: 4229.0, 2014.0: 3059.9, 5899.0: 204.2}

        atomic_number_absorber = 60

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

            self.assertAlmostEqual(macs_cm2_g[energy_eV], mac_cm2_g, 0)

    def test_absorber_promethium(self):
        """
        Test energy region 5, Z > 60.

        """
        # macs_cm2_g = {1740.0: 4511.0, 2014.0: 3252.0, 5899.0: 219.1}
        macs_cm2_g = {1740.0: 4573.6, 2014.0: 3296.5, 5899.0: 219.1}

        atomic_number_absorber = 61

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

            self.assertAlmostEqual(macs_cm2_g[energy_eV], mac_cm2_g, 0)

    def test_region6(self):
        """
        Test energy region 6.

        """
        macs_cm2_g = {2958.0: 2192.0, 3314: 1801.5, 3692.0: 1496.0}

        atomic_number_absorber = 79

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

            self.assertAlmostEqual(macs_cm2_g[energy_eV], mac_cm2_g, 0)

    def test_region6_m4(self):
        """
        Test energy region 6 with and without M4.

        """
        macs_cm2_g = {2958.0: 2192.0, 3314: 1801.5, 3692.0: 1496.0}

        atomic_number_absorber = 79

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

            self.assertAlmostEqual(macs_cm2_g[energy_eV], mac_cm2_g, 0)

        macs_cm2_g = {100.0: 100070.5, 105.0: 105933.2, 183.0: 42943.0}

        atomic_number_absorber = 31

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

            self.assertAlmostEqual(macs_cm2_g[energy_eV], mac_cm2_g, 0)

    def test_region7(self):
        """
        Test energy region 7.

        """
        macs_cm2_g = {2622.0: 2418.0, 2958: 2192.0, 3314.0: 1801.5}

        atomic_number_absorber = 79

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

            self.assertAlmostEqual(macs_cm2_g[energy_eV], mac_cm2_g, 0)

    def test_region8(self):
        """
        Test energy region 8.

        """
        macs_cm2_g = {2014.0: 1192.0, 2622.0: 2418.0, 2958: 2192.0}

        atomic_number_absorber = 79

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

            self.assertAlmostEqual(macs_cm2_g[energy_eV], mac_cm2_g, 0)

    def test_region9(self):
        """
        Test energy region 9.

        """
        macs_cm2_g = {2014.0: 1192.0, 2257.0: 1468.0, 2395.0: 3073.9}

        atomic_number_absorber = 79

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

            self.assertAlmostEqual(macs_cm2_g[energy_eV], mac_cm2_g, 0)

        mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(1490.0, 69)
        self.assertAlmostEqual(1815.0240923054969, mac_cm2_g, 0)

    def test_region10(self):
        """
        Test energy region 10.

        """
        macs_cm2_g = {849.0: 6763.5, 2014.0: 1192.0, 2257.0: 1468.0}

        atomic_number_absorber = 79

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

            self.assertAlmostEqual(macs_cm2_g[energy_eV], mac_cm2_g, 0)

    def test_region11(self):
        """
        Test energy region 11.

        .. todo:: Test energy region 11.
        """
        macs_cm2_g = {
            183.0: 14800.49302937263,
            277.0: 22962.565133671458,
            392.0: 19997.03945903206,
            677.0: 12634.929382350225,
            849.0: 6763.5}

        atomic_number_absorber = 79

        for energy_eV in macs_cm2_g:
            mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

            self.assertAlmostEqual(macs_cm2_g[energy_eV], mac_cm2_g, 0)

    def test_absorber_plutonium(self):
        """
        .. todo:: Add test for plutonium absorber.
        """

        # self.fail("Test if the TestCase is working.")

    def test_get_region(self):
        regions = {
            86.4 + 1.0: 11,
            107.8 + 1.0: 11,
            333.89 + 1.0: 11,
            351.99 + 1.0: 11,
            545.38 + 1.0: 11,
            643.67 + 1.0: 11,
            758.77 + 1.0: 10,
            2205.6 + 1.0: 9,
            2291.0 + 1.0: 8,
            2742.9 + 1.0: 7,
            3147.7 + 1.0: 6,
            3424.8 + 1.0: 5,
            11918.0 + 1.0: 4,
            13733.0 + 1.0: 3,
            14352.0 + 1.0: 2,
            80722.0 + 1.0: 1
        }

        atomic_number_absorber = 79

        for xrayEnergy_eV in regions:
            region = self.heinrich1987.get_region(atomic_number_absorber, xrayEnergy_eV)

            self.assertEqual(regions[xrayEnergy_eV], region)

        region = self.heinrich1987.get_region(atomic_number=6, xray_energy_eV=1.0)
        assert region == 2

        region = self.heinrich1987.get_region(atomic_number=79, xray_energy_eV=-50.0)
        assert region == 11

    def test_low_energy(self):
        atomic_number_absorber = 14
        energy_eV = 1.0  # noqa

        mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

        self.assertAlmostEqual(1.0E6, mac_cm2_g, 0)

        atomic_number_absorber = 79
        energy_eV = 1.0  # noqa

        mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(energy_eV, atomic_number_absorber)

        self.assertAlmostEqual(1.0E6, mac_cm2_g, 0)

        mac_cm2_g = self.heinrich1987.compute_mac_cm2_g(-50.0, atomic_number_absorber)
        self.assertAlmostEqual(1.0E6, mac_cm2_g, 0)
