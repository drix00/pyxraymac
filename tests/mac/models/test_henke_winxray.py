#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.mac.models.test_henke_winxray
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`xray.mac.models.henke_winxray` module.
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
from xray.mac.models.henke_winxray import MacHenkeWinxray
from xray.mac import get_current_module_path

# Globals and constants variables.


class TestMacHenkeWinxray(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        data_path = get_current_module_path(__file__, "../../../data/henke1993/winxray")
        if not os.path.isdir(data_path):
            pytest.skip("Data path file not found: {}".format(data_path))

        self.macData = MacHenkeWinxray(data_path)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_skeleton(self):
        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def test_constructor(self):
        data_path = get_current_module_path(__file__, "../../../data/henke1993/winxray")

        mac_data = MacHenkeWinxray(data_path)

        self.assertTrue(mac_data.pathnameBinary != "")

        self.assertTrue(mac_data.pathnameText != "")

    def test_read_text_data(self):
        enegies_eV, mac_cm2_g = self.macData.read_text_data(28)  # noqa

        self.assertEqual(500, len(enegies_eV))

        self.assertEqual(500, len(mac_cm2_g))

        self.assertEqual(10.0, enegies_eV[0])

        self.assertEqual(98739.2, mac_cm2_g[0])

        self.assertEqual(30000.0, enegies_eV[-1])

        self.assertEqual(9.77398, mac_cm2_g[-1])

    def test_read_binary_data(self):
        enegies_eV, mac_cm2_g = self.macData.read_binary_data(28)  # noqa

        self.assertEqual(500, len(enegies_eV))

        self.assertEqual(500, len(mac_cm2_g))

        self.assertAlmostEqual(10.0, enegies_eV[0], 1)

        self.assertAlmostEqual(98739.2, mac_cm2_g[0], 1)

        self.assertAlmostEqual(30000.0, enegies_eV[-1], 1)

        self.assertAlmostEqual(9.77398, mac_cm2_g[-1], 1)
