#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.mac.models.test_MacHenke
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`xray.mac.models.MacHenke` module.
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
import os.path

# Third party modules.
import pytest

# Local modules.

# Project modules.
import xray.mac.models.MacHenke as MacHenke
from xray.mac import get_current_module_path

# Globals and constants variables.


class TestMacHenke(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        configuration_file = get_current_module_path(__file__, "../MassAbsorptionCoefficient.cfg")
        if not os.path.isfile(configuration_file):
            pytest.skip("Configuration file not found")

        self.macData = MacHenke.MacHenke(configuration_file)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testConstructor(self):
        configuration_file = get_current_module_path(__file__, "../MassAbsorptionCoefficient.cfg")

        mac_data = MacHenke.MacHenke(configuration_file)

        self.assertTrue(mac_data._pathname != "")

        self.assertEquals("sf.tar.gz", mac_data._filename)

    def testReadData(self):
        enegies_eV, macs_cm2_g = self.macData.readData(28)

        self.assertAlmostEquals(10.0, enegies_eV[0])

        self.assertAlmostEquals(30000.0, enegies_eV[-1])

        self.assertAlmostEquals((9.87), macs_cm2_g[0]*1.0E-4, 2)

        self.assertAlmostEquals((9.77), macs_cm2_g[-1], 2)

    def testWavelenght(self):
        wavelengths_electron_non_relativistic_williams1996_nm = {
            100.0E3: 0.00386,
            120.0E3: 0.00352,
            200.0E3: 0.00273,
            300.0E3: 0.00223,
            400.0E3: 0.00193,
            1000.0E3: 0.00122}

        wavelengths_electron_relativistic_williams1996_nm = {
            100.0E3: 0.00370,
            120.0E3: 0.00335,
            200.0E3: 0.00251,
            300.0E3: 0.00197,
            400.0E3: 0.00164,
            1000.0E3: 0.00087}

        wavelengths_photon_A = {10.2: 1215.6, 91.5: 135.5, 14988.0: 0.8}

        for energy_eV in wavelengths_electron_non_relativistic_williams1996_nm:
            self.assertAlmostEquals(wavelengths_electron_non_relativistic_williams1996_nm[energy_eV], MacHenke.WavelenghtElectron_nm(energy_eV), 4)

            self.assertAlmostEquals(wavelengths_electron_relativistic_williams1996_nm[energy_eV], MacHenke.WavelenghtElectronRelativistic_nm(energy_eV), 4)

        for energy_eV in wavelengths_photon_A:
            self.assertAlmostEquals(wavelengths_photon_A[energy_eV] / 10.0, MacHenke.WavelenghtPhoton_nm(energy_eV), 1)

    def testComputeMac_cm2_g(self):
        mac_cm2_g = self.macData.compute_mac_cm2_g(28, 10.2, 1.14)

        self.assertAlmostEquals((8.01), mac_cm2_g*1.0E-4, 2)

        mac_cm2_g = self.macData.compute_mac_cm2_g(28, 1486.7, 8.88)

        self.assertAlmostEquals((4.28), mac_cm2_g*1.0E-3, 2)
