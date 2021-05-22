#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.mac.models.test_MacHenkeWinxray
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`xray.mac.models.MacHenkeWinxray` module.
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
import xray.mac.models.MacHenkeWinxray as MacHenkeWinxray
from xray.mac import get_current_module_path

# Globals and constants variables.


class TestMacHenkeWinxray(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        configuration_file = get_current_module_path(__file__, "../MassAbsorptionCoefficient.cfg")
        if not os.path.isfile(configuration_file):
            pytest.skip("Configuration file not found")

        self.macData = MacHenkeWinxray.MacHenkeWinxray(configuration_file)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testConstructor(self):
        configuration_file = get_current_module_path(__file__, "../MassAbsorptionCoefficient.cfg")

        mac_data = MacHenkeWinxray.MacHenkeWinxray(configuration_file)

        self.assertTrue(mac_data.pathnameBinary != "")

        self.assertTrue(mac_data.pathnameText != "")

    def testReadTextData(self):
        enegies_eV, mac_cm2_g = self.macData.readTextData(28)

        self.assertEquals(500, len(enegies_eV))

        self.assertEquals(500, len(mac_cm2_g))

        self.assertEquals(10.0, enegies_eV[0])

        self.assertEquals(98739.2, mac_cm2_g[0])

        self.assertEquals(30000.0, enegies_eV[-1])

        self.assertEquals(9.77398, mac_cm2_g[-1])

    def testReadBinaryData(self):
        enegies_eV, mac_cm2_g = self.macData.readBinaryData(28)

        self.assertEquals(500, len(enegies_eV))

        self.assertEquals(500, len(mac_cm2_g))

        self.assertAlmostEquals(10.0, enegies_eV[0], 1)

        self.assertAlmostEquals(98739.2, mac_cm2_g[0], 1)

        self.assertAlmostEquals(30000.0, enegies_eV[-1], 1)

        self.assertAlmostEquals(9.77398, mac_cm2_g[-1], 1)
