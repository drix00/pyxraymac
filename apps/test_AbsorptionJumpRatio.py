#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: test_AbsorptionJumpRatio
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for the :py:mod:`AbsorptionJumpRatio` module.
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
import AbsorptionJumpRatio as AbsorptionJumpRatio
from xray_mac.mac import get_current_module_path

# Globals and constants variables.


def test_is_discovered():
    """
    Test used to validate the file is included in the tests
    by the test framework.
    """
    assert False
    # assert True


class TestAbsorptionJumpRatio(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        configuration_file = get_current_module_path(__file__, "AbsorptionJumpRatio.cfg")
        if not os.path.isfile(configuration_file):
            pytest.skip("Configuration file not found")

        self.absorptionJumpRatio = AbsorptionJumpRatio.AbsorptionJumpRatio(configuration_file)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_skeleton(self):
        # self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testReadConfigurationFile(self):
        configuration_file = get_current_module_path(__file__, "AbsorptionJumpRatio.cfg")

        AbsorptionJumpRatio.AbsorptionJumpRatio(configuration_file)

        # self.assertEqual("pathname", absorptionJumpRatio.pathname)

    def testCopper(self):
        jump_factor_LI = 0.1174

        jump_factor_LIK = 0.1743

        jump_factor = self.absorptionJumpRatio.get_absorption_jump_factor(29, 'LI', 1200.0)

        self.assertAlmostEqual(jump_factor_LI, jump_factor, 3)

        jump_factor = self.absorptionJumpRatio.get_absorption_jump_factor(29, 'LI', 12000.0)

        self.assertAlmostEqual(jump_factor_LIK, jump_factor, 3)

    def testFEL3Al(self):
        jump_factor_reference = 0.49363

        jump_factor = self.absorptionJumpRatio.get_absorption_jump_factor(26, 'L3', 1486.9)

        self.assertAlmostEqual(jump_factor_reference, jump_factor, 3)
