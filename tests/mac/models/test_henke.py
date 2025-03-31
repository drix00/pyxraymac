#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.mac.models.test_henke
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`xray_mac.mac.models.henke` module.
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
from xray_mac.mac.models.henke import MacHenke
from xray_mac.mac.models.henke import wavelength_electron_nm, wavelength_electron_relativistic_nm, wavelength_photon_nm
from xray_mac.mac import get_current_module_path

# Globals and constants variables.


class TestMacHenke(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        data_path = get_current_module_path(__file__, "../../../data/henke1993/data")
        if not os.path.isdir(data_path):  # pragma: no cover
            pytest.skip("Data path file not found: {}".format(data_path))

        self.macData = MacHenke(data_path)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_skeleton(self):
        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def test_constructor(self):
        data_path = get_current_module_path(__file__, "../../../data/henke1993/data")

        mac_data = MacHenke(data_path)

        self.assertTrue(mac_data.data_path != "")

        self.assertEqual("sf.tar.gz", mac_data._filename)

    def test_read_data(self):
        enegies_eV, macs_cm2_g = self.macData.read_data(28)  # noqa

        self.assertAlmostEqual(10.0, enegies_eV[0])

        self.assertAlmostEqual(30000.0, enegies_eV[-1])

        self.assertAlmostEqual(9.87, macs_cm2_g[0]*1.0E-4, 2)

        self.assertAlmostEqual(9.77, macs_cm2_g[-1], 2)

    def test_wavelength(self):
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

        wavelengths_photon_A = {10.2: 1215.6, 91.5: 135.5, 14988.0: 0.8}  # noqa

        for energy_eV in wavelengths_electron_non_relativistic_williams1996_nm:
            self.assertAlmostEqual(wavelengths_electron_non_relativistic_williams1996_nm[energy_eV],
                                   wavelength_electron_nm(energy_eV), 4)

            self.assertAlmostEqual(wavelengths_electron_relativistic_williams1996_nm[energy_eV],
                                   wavelength_electron_relativistic_nm(energy_eV), 4)

        for energy_eV in wavelengths_photon_A:
            self.assertAlmostEqual(wavelengths_photon_A[energy_eV] / 10.0, wavelength_photon_nm(energy_eV), 1)

    def test_compute_mac_cm2_g(self):
        mac_cm2_g = self.macData.compute_mac_cm2_g(28, 10.2, 1.14)

        self.assertAlmostEqual(8.01, mac_cm2_g*1.0E-4, 2)

        mac_cm2_g = self.macData.compute_mac_cm2_g(28, 1486.7, 8.88)

        self.assertAlmostEqual(4.28, mac_cm2_g*1.0E-3, 2)
