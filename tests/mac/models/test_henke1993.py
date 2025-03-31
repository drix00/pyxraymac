#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.mac.models.test_henke1993
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`xray_mac.mac.models.henke1993` module.
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
import os.path
import unittest

# Third party modules.
import pytest

# Local modules.

# Project modules.
from xray_mac.mac import get_current_module_path
from xray_mac.mac.models.henke1993 import MacHenke1993

# Globals and constants variables.


class TestMacHenke1993(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        data_path = get_current_module_path(__file__, "../../../data/henke1993/data")
        if not os.path.isdir(data_path):  # pragma: no cover
            pytest.skip("Data path file not found: {}".format(data_path))

        self.mac = MacHenke1993(data_path)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_skeleton(self):
        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def test_constructor(self):
        data_path = get_current_module_path(__file__, "../../../data/henke1993/data")

        mac = MacHenke1993(data_path)
        self.assertTrue(len(mac.mac_data) == 0)

    def test_compute_mac_cm2_g(self):
        mac_cm2_g = self.mac.compute_mac_cm2_g(10.2, 28)

        self.assertAlmostEqual(9.709, mac_cm2_g*1.0E-4, 2)

        mac_cm2_g = self.mac.compute_mac_cm2_g(1486.7, 28)

        self.assertAlmostEqual(4.285, mac_cm2_g*1.0E-3, 2)

    def test_copper_m_edges(self):
        mac1_cm2_g = self.mac.compute_mac_cm2_g(130.0, 29)

        mac2_cm2_g = self.mac.compute_mac_cm2_g(115.0, 29)

        mac3_cm2_g = self.mac.compute_mac_cm2_g(50.0, 29)

        # Normal behavior if the M edge is present in the data.
        # For Henke data, the M edge is not present.
        # self.assertTrue(mac1_cm2_g > mac2_cm2_g)
        # self.assertTrue(mac2_cm2_g > mac3_cm2_g)
        # self.assertTrue(mac1_cm2_g > mac3_cm2_g)

        self.assertAlmostEqual(5.839230, mac1_cm2_g*1.0E-4, 2)

        self.assertAlmostEqual(6.1090, mac2_cm2_g*1.0E-4, 2)

        self.assertAlmostEqual(7.58129, mac3_cm2_g*1.0E-4, 2)
