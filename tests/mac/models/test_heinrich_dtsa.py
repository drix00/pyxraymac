#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: tests.mac.models.test_heinrich_dtsa
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`xray.mac.models.heinrich_dtsa` module.
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
from xray.mac.models.heinrich_dtsa import MacHeinrichDTSA

# Globals and constants variables.


class TestMacHeinrichDTSA(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.macModel = MacHeinrichDTSA()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_skeleton(self):
        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def test_compute_mac_cm2_g(self):
        value = self.macModel.computeMac_cm2_g(1041.0, 79)

        self.assertAlmostEqual(4698.6, value, 1)
