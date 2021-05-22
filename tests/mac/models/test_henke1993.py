#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.mac.models.test_henke1993
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`xray.mac.models.henke1993` module.
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
from xray.mac import get_current_module_path
import xray.mac.models.henke1993 as MacHenke1993

# Globals and constants variables.


class TestMacHenke1993(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        configuration_file = get_current_module_path(__file__, "../testdata/Databases.cfg")
        if not os.path.isfile(configuration_file):
            pytest.skip("Configuration file not found")

        self.mac = MacHenke1993.MacHenke1993(configuration_file)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testConstructor(self):
        configuration_file = get_current_module_path(__file__, "../testdata/Databases.cfg")

        mac = MacHenke1993.MacHenke1993(configuration_file)
        self.assertTrue(True)

    def testComputeMac_cm2_g(self):
        mac_cm2_g = self.mac.computeMac_cm2_g(10.2, 28)

        self.assertAlmostEquals((9.709), mac_cm2_g*1.0E-4, 2)

        mac_cm2_g = self.mac.computeMac_cm2_g(1486.7, 28)

        self.assertAlmostEquals((4.285), mac_cm2_g*1.0E-3, 2)

    def testCopperMEdges(self):
        mac1_cm2_g = self.mac.computeMac_cm2_g(130.0, 29)

        mac2_cm2_g = self.mac.computeMac_cm2_g(115.0, 29)

        mac3_cm2_g = self.mac.computeMac_cm2_g(50.0, 29)

        # Normal behavior if the M edge is present in the data.
        # For Henke data, the M edge is not present.
        # self.assertTrue(mac1_cm2_g > mac2_cm2_g)
        # self.assertTrue(mac2_cm2_g > mac3_cm2_g)
        # self.assertTrue(mac1_cm2_g > mac3_cm2_g)

        self.assertAlmostEquals((5.839230), mac1_cm2_g*1.0E-4, 2)

        self.assertAlmostEquals((6.1090), mac2_cm2_g*1.0E-4, 2)

        self.assertAlmostEquals((7.58129), mac3_cm2_g*1.0E-4, 2)
